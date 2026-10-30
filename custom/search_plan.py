"""Profile-driven offline discovery plan. Never searches, applies or schedules."""
import argparse
from datetime import datetime, timedelta, date
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.parse import urlencode
import json

ROOT=Path(__file__).resolve().parents[1]
DOMAINS=['jobs.ashbyhq.com','job-boards.greenhouse.io','boards.greenhouse.io','jobs.lever.co','myworkdayjobs.com','jobs.smartrecruiters.com']

def build(profile, day):
    rows=[]
    families=list(profile['role_families'].items())
    locations=profile['location_groups']
    for d,domain in enumerate(DOMAINS):
        for f,(name,titles) in enumerate(families):
            location=locations[(day.toordinal()+d+f)%len(locations)]
            # DFW uses alternative city names, not a single exact phrase.
            geo='(Dallas OR Plano OR Irving OR Frisco)' if location.startswith('Dallas ') else '"'+location+'"'
            q=f'site:{domain} ('+' OR '.join('"'+t+'"' for t in titles)+f') {geo} after:{(day-timedelta(days=7)).isoformat()}'
            rows.append({'id':f'{domain}:{name}','source':'ATS index','query':q,'location_scope':location,'status':'not_run','url':'https://www.google.com/search?'+urlencode({'q':q})})
        name,titles=families[day.toordinal()%len(families)]
        q=f'site:{domain} ('+' OR '.join('"'+t+'"' for t in titles)+') United States'
        rows.append({'id':f'{domain}:recall','source':'ATS recall','query':q,'location_scope':'United States broad recall','status':'not_run','url':'https://www.google.com/search?'+urlencode({'q':q})})
    return {'as_of':day.isoformat(),'timezone':profile['timezone'],'status':'planned_not_executed','coverage_note':'24 recent queries rotate location assignments; six broad recall queries. Not every role/location/domain combination is covered. Search dates are not official posting dates.','queries':rows}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,default=ROOT/'config/search-profile.example.json')
    parser.add_argument('--date',type=date.fromisoformat)
    parser.add_argument('--output',type=Path,default=ROOT/'.local/search-plan.json')
    args=parser.parse_args()
    profile=json.loads(args.profile.read_text())
    result=build(profile,args.date or datetime.now(ZoneInfo(profile['timezone'])).date())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(f"Saved {len(result['queries'])} planned queries: {args.output}")
if __name__=='__main__': main()
