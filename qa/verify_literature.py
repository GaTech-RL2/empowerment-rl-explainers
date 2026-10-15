"""Check literature filtering, direct links, and responsive layout."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
    page=b.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8772/literature.html',wait_until='networkidle')
    assert page.locator('.paper:visible').count()==19
    page.locator('[data-filter=eysenbach]').click();assert page.locator('.paper:visible').count()==8
    page.locator('#paper-search').fill('Shortcut Learning');assert page.locator('.paper:visible').count()==1
    page.locator('#paper-search').fill('nonexistent-example');assert page.locator('.paper:visible').count()==0
    page.locator('.reading-path a').nth(1).click();assert page.locator('.paper:visible').count()==19
    assert page.evaluate('location.hash')=='#symbols'
    page.goto('http://127.0.0.1:8772/literature.html');page.screenshot(path=str(ROOT/'qa/literature-desktop.png'))
    page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
    page.screenshot(path=str(ROOT/'qa/literature-mobile.png'))
    page.goto('http://127.0.0.1:8772/');assert page.locator('.research-callout a').get_attribute('href')=='literature.html'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
    assert not errors,errors
    report={'paper_count':19,'eysenbach_count':8,'filter_and_search':'passed','direct_links':'passed','mobile_overflow':False,'page_errors':errors}
    (ROOT/'qa/literature-report.json').write_text(json.dumps(report,indent=2)+'\n');print(report);b.close()
