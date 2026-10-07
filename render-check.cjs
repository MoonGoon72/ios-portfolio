const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const path = require('path');
const os = require('os');
(async () => {
 const browser = await chromium.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE || undefined});
 const page = await browser.newPage({viewport:{width:1440,height:1050}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8765/',{waitUntil:'networkidle'});
 await page.evaluate(()=>document.fonts.ready);
 await page.evaluate(()=>{document.querySelectorAll('img').forEach(x=>x.loading='eager');});
 await page.evaluate(()=>Promise.all([...document.images].map(img=>img.decode().catch(()=>{}))));
 await page.screenshot({path:path.join(os.tmpdir(),'portfolio-desktop.png')});
 await page.locator('.screens.tk8').first().screenshot({path:path.join(os.tmpdir(),'portfolio-apps.png')});
 await page.locator('.feature-gallery').screenshot({path:path.join(os.tmpdir(),'portfolio-features.png')});
 await page.locator('.todakun-intro').screenshot({path:path.join(os.tmpdir(),'portfolio-todakun.png')});
 const checks=[];
 for (const width of [1440,768,390]){
  await page.setViewportSize({width,height:900});
  await page.evaluate(()=>window.scrollTo(0,0));
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
  const broken=await page.locator('img').evaluateAll(xs=>xs.filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.src));
  checks.push({width,overflow,broken});
 }
 await page.screenshot({path:path.join(os.tmpdir(),'portfolio-mobile.png')});
 const count=await page.locator('.case').count();
 const firstClosed=page.locator('.case').nth(1);
 await firstClosed.locator('summary').click();
 const opened=await firstClosed.evaluate(el=>el.open);
 checks.push({cases:count,detailToggle:opened,jsErrors:errors});
 if(checks.some(x=>x.overflow || x.broken?.length) || !opened || errors.length) throw new Error(JSON.stringify(checks));
 await page.setViewportSize({width:1440,height:1050});
 await page.evaluate(()=>{document.querySelectorAll('details').forEach(x=>x.open=true);document.querySelectorAll('img').forEach(x=>x.loading='eager');});
 await page.evaluate(()=>Promise.all([...document.images].map(img=>img.decode().catch(()=>{}))));
 await page.emulateMedia({media:'print'});
 await page.pdf({path:path.join(__dirname,'dist/portfolio.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<div></div>',footerTemplate:'<div style="font-family:Arial,sans-serif;font-size:8px;width:100%;color:#58677c;margin:0 17mm;display:flex;justify-content:space-between;"><span>Younggyun Mun / Portfolio / 2026</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'});
 console.log(JSON.stringify(checks));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
