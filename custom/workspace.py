"""Create an isolated private workspace or build an explicitly fictional public demo."""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
PANEL=Path('工具/求职进度面板')

def customize(page, demo=False):
    text=page.read_text()
    text=text.replace('<title>求职面板</title>','<title>Career Compass | 分析岗求职面板</title>')
    text=text.replace('<h1>求职面板</h1>','<h1>Career Compass · 分析岗求职面板</h1>')
    text=text.replace('var TABS = ["today", "discovered", "todo", "progress", "internships"];','var TABS = ["today", "discovered", "todo", "progress"];')
    text=text.replace('医疗 AI 扫描池','可选岗位扫描池')
    text=text.replace('（从 vault 投递记录 + Gmail 核对整理）','（仅展示实际导入并核验的本地记录）')
    text=text.replace('改数据后运行 python3 工具/求职进度面板/make_dashboard.py --open 重新生成。','改数据后在项目根目录运行 python3 custom/workspace.py build 重新生成。')
    if demo:
        label='演示模式 · 公司、申请、面试和结果均为虚构示例；不是 Harry 的真实经历。'
    else:
        label='私人工作区 · 本页含本地记录，请勿上传或公开分享。'
    text=text.replace('<nav class="tabs"',f'<div role="note" style="padding:12px 16px;background:#e8f0ff;border:1px solid #9cb9ef;border-radius:10px;margin:16px 0;color:#173b68">{label}</div><nav class="tabs"')
    page.write_text(text)

def prepare_runtime(dest):
    board=dest/'工具/healthcare岗位抓取/render_board.py'
    code=(ROOT/'工具/healthcare岗位抓取/render_board.py').read_text()
    start=code.index('ROLES = ')
    end=code.index('ROLE_OF_FAMILY = ',start)
    code=code[:start]+'ROLES = {"business": "商业 / 数据分析", "growth": "增长 / 营销分析", "product": "产品 / 收入分析", "gtm": "GTM / 策略分析", "other": "其他"}\n'+code[end:]
    code=code.replace('    t = title or ""', '    t = title or ""\n    if re.search(r"gtm|sales strategy|strategy.*operations",t,re.I): return "gtm"\n    if re.search(r"growth|marketing|advertising",t,re.I): return "growth"\n    if re.search(r"product|revenue|monetization",t,re.I): return "product"\n    if re.search(r"business|data analyst|bi analyst",t,re.I): return "business"')
    code=code.replace('"dfw": 15, "remote": 15, "remote_state": 8, "tx": 10','"dfw": 0, "remote": 0, "remote_state": 0, "tx": 0')
    board.write_text(code)
    engine=dest/PANEL/'make_dashboard.py'
    engine.write_text(engine.read_text().replace('America/Chicago','America/Los_Angeles'))

def private_init():
    dest=ROOT/'.local/private'
    if dest.exists(): raise SystemExit('Private workspace already exists; left unchanged.')
    shutil.copytree(ROOT/'工具',dest/'工具',ignore=shutil.ignore_patterns('__pycache__','*.json','dashboard.html','board.html','raw','out','logs','manual','ref'))
    panel=dest/PANEL
    for filename,data in {'applications.json':{'updated':'2026-10-30','gmail_account':'','applications':[]},'targets.json':{'targets':[]},'internships.json':{'updated':'2026-10-30','items':[]}}.items():
        (panel/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2))
    (dest/'工具/healthcare岗位抓取/pool_board.json').write_text('{"items": []}')
    shutil.copyfile(ROOT/'config/search-profile.example.json',dest/'profile.json')
    print('Created empty private workspace:',dest)

def build(demo=False):
    if demo:
        subprocess.run([sys.executable,str(ROOT/'scripts/demo.py')],cwd=ROOT,check=True)
        panel=ROOT/'.local/demo'/PANEL
        # Modify fictional fixtures only. Never read private inputs while building demo.
        prepare_runtime(ROOT/'.local/demo')
        replacements={'Research Scientist':'Marketing Analyst','Machine Learning Engineer':'Business Analyst','Applied Scientist':'Growth Analyst','ML Engineer':'GTM Analyst','Research Engineer':'Revenue Analyst','Data Scientist':'Data Analyst','Imaging Research Scientist':'Product Analyst'}
        for filename in ['applications.json','targets.json']:
            p=panel/filename
            obj=json.loads(p.read_text())
            for item in obj.get('applications',obj.get('targets',[])):
                item['title']=replacements.get(item.get('title'), 'Product Analyst')
            p.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
        (panel/'internships.json').write_text('{"updated":"2026-10-27","items":[]}')
        subprocess.run([sys.executable,str(panel/'make_dashboard.py'),'--today','2026-10-27'],check=True)
        customize(panel/'dashboard.html',True)
        (ROOT/'demo').mkdir(exist_ok=True)
        shutil.copyfile(panel/'dashboard.html',ROOT/'demo/index.html')
        print('Public fictional demo:',ROOT/'demo/index.html')
    else:
        panel=ROOT/'.local/private'/PANEL
        if not panel.exists(): raise SystemExit('Run init first.')
        prepare_runtime(ROOT/'.local/private')
        # Patch only the isolated runtime copy: empty history is a valid first run.
        engine=panel/'make_dashboard.py'
        code=(ROOT/PANEL/'make_dashboard.py').read_text()
        code=code.replace('if not isinstance(apps, list) or not apps:', 'if not isinstance(apps, list):')
        code=code.replace('min(a["first_out"] for a in apps)', 'min((a["first_out"] for a in apps), default=today.isoformat())')
        code=code.replace('max(a["last_any"]["date"] for a in apps)', 'max((a["last_any"]["date"] for a in apps), default=today.isoformat())')
        code=code.replace('America/Chicago','America/Los_Angeles')
        engine.write_text(code)
        subprocess.run([sys.executable,str(engine)],check=True)
        customize(panel/'dashboard.html')
        print('Private dashboard:',panel/'dashboard.html')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['init','build','demo'])
    command=p.parse_args().command
    if command=='init': private_init()
    else: build(command=='demo')
