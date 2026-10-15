"""Browser acceptance checks, including mobile layout and numeric parity."""
import json,sys,math
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import empowerment_lab as M
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8772/'

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(URL,wait_until='networkidle');page.screenshot(path=str(ROOT/'qa/desktop.png'),full_page=True)
    reports=[]
    for i in range(6):
        page.evaluate('(i)=>Course.selectEpisode(i)',i)
        page.wait_for_function('document.querySelector("video").readyState >= 1')
        assert abs(page.eval_on_selector('video','v=>v.duration')-420)<.15
        assert page.locator('.chapter-button').count()==6
        page.evaluate('Course.seekChapter(5)')
        page.wait_for_function('document.querySelector("video").currentTime > 300')
        page.evaluate('Course.selectTab("notes")')
        assert page.locator('.chapter-note').count()==6
        assert page.locator('.derivation').count()==18
        page.evaluate('Course.selectTab("lab")')
        assert page.locator('table tbody tr').count()>0
        assert 'def capacity' in page.locator('.code-panel pre').text_content()
        for slider in page.locator('input[type=range]').all():
            for end in ('min','max'):
                slider.evaluate('(e,end)=>{e.value=e[end];e.dispatchEvent(new Event("input",{bubbles:true}))}',end)
                text=page.locator('#lab-metrics').inner_text()
                assert 'NaN' not in text and 'Infinity' not in text,(i,text)
            page.locator('#reset-lab').click()
        page.screenshot(path=str(ROOT/f'qa/lab-{i+1}.png'),full_page=True)
        reports.append({'episode':i+1,'duration':420,'chapters':6,'derivations':18,'sliders':'all boundaries passed'})
    # Exact agreement between independently implemented Python and JS formulas.
    fixtures=[]
    for k in [2,3,5]:
        for noise in [0,.17,.5,1]:
            W=M.symmetric(k,noise);p0=[1/k]*k
            fixtures.append({'W':W,'p':p0,'I':M.mutual_information(W,p0),'B':M.variational_bound(W,p0,.62),'C':M.capacity(W)['value']})
    fixtures.append({'W':[[1,0],[.5,.5]],'p':[.1,.9],'I':M.mutual_information([[1,0],[.5,.5]],[.1,.9]),'B':M.variational_bound([[1,0],[.5,.5]],[.1,.9],.62),'C':math.log(1.25)})
    numeric=page.evaluate('''fixtures=>fixtures.map(f=>({I:LabModels.MI(f.W,f.p),B:LabModels.bound(f.W,f.p,.62),C:LabModels.capacity(f.W).value}))''',fixtures)
    for f,r in zip(fixtures,numeric):
        for key in ('I','B','C'):assert abs(f[key]-r[key])<2e-8,(f,r,key)
    assert page.evaluate('LabModels.threshold([.5], Math.log(2)).accepted')==0
    mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
    mobile.goto(URL,wait_until='networkidle')
    for tab in ['watch','lab','notes']:
        mobile.evaluate('(t)=>Course.selectTab(t)',tab)
        assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),tab
        mobile.screenshot(path=str(ROOT/f'qa/mobile-{tab}.png'),full_page=True)
    # File-based use must not require a server for the labs or local math.
    if URL.startswith('http://127.'):
        offline=browser.new_page();offline.goto((ROOT/'index.html').as_uri())
        offline.evaluate('Course.selectTab("lab")')
        assert offline.locator('table tbody tr').count()>0
        offline.evaluate('Course.selectTab("notes")')
        offline.wait_for_function('Array.from(document.querySelectorAll(".derivation img")).filter(i=>i.getBoundingClientRect().height>0).every(i=>i.complete && i.naturalWidth>0)')
    assert not errors,errors
    report={'url':URL,'episodes':reports,'numeric_parity_fixtures':len(fixtures),'mobile':'watch, lab, notes: no page overflow','page_errors':errors}
    (ROOT/'qa/site-report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2));browser.close()
