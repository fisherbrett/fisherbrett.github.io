---
title: How I Used JavaScript to Scrape Over 8000 Chinese Characters
date: '2020-07-18T23:46:37.121Z'
layout: post
---

At the beginning of 2019, I decided to sign up for a Mandarin Chinese 101 class at my university. Studying Chinese has since become one of my favorite pastimes, and to this day I continue to take private lessons via [italki](https://www.italki.com/).

As I progressed in my speaking skills, I started paying more attention to the structure of Chinese characters. You see, each Chinese character can contain and represent a lot of information. For example, many characters contain two parts - a "radical", which indicates the meaning of the character, and a "component", which gives a clue as to how the character should be pronounced. There is also something called the HSK level of a character. China has created a test called the HSK which assesses the proficiency of Mandarin learners. It contains 6 levels, where 1 is the easiest and 6 is the hardest. Many of the characters are grouped into one of these 6 levels, and sometimes it's helpful to know a character's level. Since I've practiced Chinese for a little while but definitely still feel like a beginner, I like to focus on HSK 1 and 2 level characters since they're typically more common than, say, level 5 or 6 characters.

I've found a couple of mobile apps that have been particularly helpful in helping me learn and study Chinese characters - a couple of my favorites are [Pleco](https://www.pleco.com/) for looking up words/characters and [Du Chinese](https://www.duchinese.net/) for practicing my reading skills. However, I haven't yet been able to find a website with a clean, modern, and flexible search interface. There are a few websites with a lot of great character information, but the UI looks like it was made in the 90's and the page loads are slow.

That's definitely not to say that all Chinese character websites out there are bad - there are ones that provide good information about words I don't know, but now I almost exclusively use the Pleco app as a dictionary because it's so good. What it doesn't do is allow the kind of advanced searches that I'm interested in. The information I'm most interested in for each character is its pinyin (how it's pronounced spelled out with English letters) and its frequency (where a frequency of 1 would be the most commonly used character). Other information I find helpful is the HSK level and the stroke count, or how many pen strokes it takes to write the character. A smaller stroke count means its probably easier to remember how to write it!

None of the apps I use or any website I've found has allowed me to do things like get a list of all HSK level 2 characters with a stroke count of less than 10, or the top 20 most frequently occurring characters containing the radical 氵(which usually indicates the character's meaning has something to do with water). As a web developer, I found this to be unacceptable! I figured if I had a list of Chinese characters with the information I wanted, it would be pretty simple to import them into a spreadsheet and then perform basic queries on them. Even better, I could create a GraphQL server that would allow for some really sweet flexibility.

But first, I needed a list of characters. After some digging around on the internet, I found the [hanziDB website](http://hanzidb.org/character-list/general-standard?page=1) which contains over 8000 Chinese characters along with their meaning, pronounciation, radical, stroke count, HSK level, and frequency! Seeing how you [only need to know 1500 - 2000 characters to be considered fluent in Mandarin](https://www.fluentu.com/blog/chinese/2018/09/19/how-many-chinese-characters-do-i-need-to-know/), this list was more than enough. Now I just needed to download all the data on the hanziDB site so I would be able to query it as I pleased.

## Cheerio to the Rescue

In the past, I did some web scraping using the Python [requests](https://requests.readthedocs.io/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) libraries. Both of those worked out great, but since I've recently become a JavaScript addict, I wanted to challenge myself and see if I could scrape the Chinese character data using JS.

A simple Google search taught me about [cheerio](https://cheerio.js.org/), a Node module which can parse HTML using jQuery syntax. I decided I would query the hanziDB site with [axios](https://www.npmjs.com/package/axios) and extract the character information I wanted with cheerio before saving everything to a text file.

Since axios and cheerio were the only dependencies I needed, it was pretty easy to create a quick Node project:

```bash
$ mkdir character-scraper && cd character-scraper
$ yarn init -y
$ yarn add cheerio axios
$ touch index.js
```

At the top of my `index.js` file I added the following lines:

```js
const axios = require('axios').default;
const cheerio = require('cheerio');
const fs = require('fs');
```

I `require`d `fs` so that I'll be able to write the extracted data to a text file. I then decided to first write a simple function that could query a single page of characters. Looking at the table, I could see that there were 82 pages of characters in total.

![82 pages of Chinese characters](/assets/82pages.png)

I also noticed that when I changed the page, it would reflect in the URL with a query parameter called `page`. For example, if I changed to page 3, the URL would be http://hanzidb.org/character-list/general-standard?page=3.

That made writing a `getPage` function super easy:

```js
async function getPage(pageNum) {
  const url = `http://hanzidb.org/character-list/general-standard?page=${pageNum}`;
  const { data: html } = await axios.get(url);
  return html;
}
```

That function returns the HTML at a given page number. Next I needed a function that would actually parse out the Chinese character information contained in the table. This was where things got a little tricky, but not too bad. After inspecting the HTML in the Chrome developer tools, I realized that the table contained a `<tbody>` element which happened to be the only `<tbody>` element on the page! That made writing the CSS selectors a lot easier. I realized I could just use [nth-child](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child) to select the specific row and column I wanted in the table. My `extractPageData` function looks like this:

```js
function extractPageData(pageData) {
  const $ = cheerio.load(pageData);

  const numRows = $('tbody tr').length;

  const pageVals = [];
  for (let row = 2; row <= numRows; row++) {
    const colVals = [];
    for (let col = 1; col <= 8; col++) {
      colVals.push($(`tbody tr:nth-child(${row}) td:nth-child(${col})`).text());
    }
    pageVals.push(colVals.join('\t'));
  }

  return pageVals.join('\n');
}
```

I set the `row` to 2 because the first row will always contain the header information, like "Pinyin", "Definition", etc. That will always be the same, so I ignored it. There are 8 columns, so I then looped over each column in each row and extracted the text using cheerio's `text()` method. I stored the data in each row in an array called `colVals`. I `join`ed each `colVals` array with a tab and inserted it into a `pageVals` array. The function returns the `pageVals` array joined by newlines. That will get all the information I want from a certain page!

Finally, I needed a function to actually query each of the 82 pages, parse the data with `extractPageData`, and write everything to a file. That function was pretty easy to write as well:

```js
async function scrapeData() {
  const pageDataPromises = [];

  for (let i = 1; i <= 82; i++) {
    pageDataPromises.push(getPage(i));
    if (i % 10 == 0) {
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }

  const pageData = await Promise.all(pageDataPromises);
  const pageDataCsv = pageData.map(extractPageData);
  fs.writeFileSync('characters.tsv', pageDataCsv.join('\n'));
  console.log('done');
}
```

For each of the 82 pages, I push the `Promise` returned by `getPage` into an array and use `Promise.all()` to wait for all of them to resolve. Take note of the `if` statement on the 6th line checking if the page is a multiple of 10. If it is, the program pauses for 2 seconds. I did this because the first time I tried running this function, I got a [429 error](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) for sending too many requests. Pausing every few requests fixed that.

After waiting for all the `getPage` promises to resolve, I was left with an array of all the HTML for each page. I then used JS's `map` function to run `extractPageData` on each page and then wrote everything to the `characters.tsv` file.

All that's left is to call the `scrapeData` function:

```js
scrapeData();
```

And that's it! After running the script with `node index.js`, it took about 30 or 40 seconds on my machine to download everything to a .tsv file. Then I opened the file with Google Sheets and used filters to query to my heart's content! Here's the whole script in one piece:

```js
const axios = require('axios').default;
const cheerio = require('cheerio');
const fs = require('fs');

async function getPage(pageNum) {
  const url = `http://hanzidb.org/character-list/general-standard?page=${pageNum}`;
  const { data: html } = await axios.get(url);
  return html;
}

function extractPageData(pageData) {
  const $ = cheerio.load(pageData);

  const numRows = $('tbody tr').length;

  const pageVals = [];
  for (let row = 2; row <= numRows; row++) {
    const colVals = [];
    for (let col = 1; col <= 8; col++) {
      colVals.push($(`tbody tr:nth-child(${row}) td:nth-child(${col})`).text());
    }
    pageVals.push(colVals.join('\t'));
  }

  return pageVals.join('\n');
}

async function scrapeData() {
  const pageDataPromises = [];

  for (let i = 1; i <= 82; i++) {
    pageDataPromises.push(getPage(i));
    if (i % 10 == 0) {
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }

  const pageData = await Promise.all(pageDataPromises);
  const pageDataCsv = pageData.map(extractPageData);
  fs.writeFileSync('characters.tsv', pageDataCsv.join('\n'));
  console.log('done');
}

scrapeData();
```

## Next steps

Google Sheets lets me query more easily than I was able to on the actual hanziDB site, but we can do better. I've recently been working on a GraphQL server to make all kinds of queries possible on this dataset. Once that's done, I could even use Material UI to create a frontend that would make advanced queries even easier. It's still a work in progress, but I'll probably write more about it when it's done!
