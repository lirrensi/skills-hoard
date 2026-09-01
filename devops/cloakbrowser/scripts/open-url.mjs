import { launch } from 'cloakbrowser'

const url = process.argv[2] || 'https://example.com'
const headed = process.argv.includes('--headed')
const humanize = process.argv.includes('--humanize')

const browser = await launch({
  headless: !headed,
  humanize,
})

const page = await browser.newPage()
await page.goto(url)
console.log(await page.title())
await browser.close()
