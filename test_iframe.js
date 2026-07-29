const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  const url = "https://www.owlbear.rodeo/room/MA4u6S9l2v9K/The%20Jazzy%20Loon";
  
  console.log(`Navigating to ${url}...`);
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
  
  // Wait a bit for dynamic content and iframes to load
  await new Promise(r => setTimeout(r, 5000));
  
  // Log all iframes found
  const frames = page.frames();
  console.log(`Found ${frames.length} frames.`);
  
  for (const frame of frames) {
    console.log(`Frame URL: ${frame.url()}`);
    if (frame.url().includes('character') || frame.url().includes('sheet')) {
       console.log('Found character sheet iframe.');
       try {
           const scrollInfo = await frame.evaluate(() => {
               const el = document.scrollingElement || document.body;
               return {
                   scrollHeight: el.scrollHeight,
                   clientHeight: el.clientHeight,
                   canScroll: el.scrollHeight > el.clientHeight
               };
           });
           console.log('Scroll Info:', scrollInfo);
       } catch (e) {
           console.log('Error evaluating inside frame:', e);
       }
    }
  }

  await browser.close();
})();
