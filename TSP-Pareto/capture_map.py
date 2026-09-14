import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    html_path = 'file:///home/andy/VibeCoding/ScrapingLokasi/TSP-Pareto/peta_rute_tsp_pareto.html'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        print(f"Membuka {html_path}...")
        await page.goto(html_path)
        
        # Tunggu peta Leaflet me-render tiles dan polyline
        print("Menunggu peta di-render...")
        await page.wait_for_timeout(3000)
        
        # Ambil screenshot
        output_path = 'Screenshot_Peta_TSP.png'
        await page.screenshot(path=output_path, full_page=True)
        print(f"Screenshot berhasil disimpan di: {output_path}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
