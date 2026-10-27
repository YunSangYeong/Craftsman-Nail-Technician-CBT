import { expect, test } from '@playwright/test';

for (const viewport of [{width:390,height:480},{width:740,height:360},{width:390,height:480,zoom:true}]) {
 for (const input of ['wheel','touch'] as const) {
  test(`메뉴 실제 ${input}: ${viewport.width}×${viewport.height}${viewport.zoom?' 글자 확대':''}`, async ({page, context}) => {
   await page.setViewportSize(viewport);
   await page.goto('');
   if(viewport.zoom) await page.addStyleTag({content:'html {font-size:125%} .sidebar {font-size:125%} .sidebar nav button {font-size:1.15em}'});
   await page.getByRole('button',{name:'메뉴 열기'}).click();
   const sidebar=page.locator('.sidebar');
   await expect(sidebar).toHaveClass(/open/);
   await page.waitForTimeout(400);
   const box=await sidebar.boundingBox(); expect(box).not.toBeNull();
   const x=box!.x+box!.width/2;
   const session=await context.newCDPSession(page);
   await session.send('Emulation.setTouchEmulationEnabled',{enabled:true});
   async function scroll(down:boolean) {
    if(input==='wheel') {await page.mouse.move(x,viewport.height/2); await page.mouse.wheel(0,down?500:-500);}
    else {
     const from=down?viewport.height-55:85,to=down?85:viewport.height-55;
     await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y:from}]});
     for(let n=1;n<=12;n++) {
      await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y:from+(to-from)*n/12}]});
      await page.waitForTimeout(20);
     }
     await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
    }
    await page.waitForTimeout(300);
   }
   const backup=page.getByRole('button',{name:'학습 기록 백업'});
   const reset=page.getByRole('button',{name:'데이터 초기화',exact:true});
   for(let n=0;n<5;n++) await scroll(true);
   expect(await sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
   await expect(backup).toBeInViewport(); await expect(reset).toBeInViewport();
   const download=page.waitForEvent('download'); await backup.click(); expect((await download).suggestedFilename()).toContain('nail');
   await reset.click(); await expect(page.getByRole('dialog')).toBeVisible();
   await page.getByRole('button',{name:'돌아가기',exact:true}).click();
   // Menu remains open on cancelled reset; scrolling upward must reveal the first item.
   if(!(await sidebar.getAttribute('class'))?.includes('open')) await page.getByRole('button',{name:'메뉴 열기'}).click();
   await page.waitForTimeout(400);
   for(let n=0;n<5;n++) await scroll(false);
   expect(await sidebar.evaluate(el=>el.scrollTop)).toBe(0);
   const dashboard=page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true});
   await expect(dashboard).toBeInViewport(); await dashboard.click();
   await expect(page.getByRole('heading',{name:'미용사(네일) 필기 CBT',exact:true})).toBeVisible();
   await expect(sidebar).not.toHaveClass(/open/);
   expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  });
 }
}
