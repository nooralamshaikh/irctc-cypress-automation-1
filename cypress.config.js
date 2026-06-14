const { defineConfig } = require("cypress");

const irctcClientHeaders = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
  "accept-language": "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-US;q=0.6",
  "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": '"Windows"',
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "none",
  "sec-fetch-user": "?1",
  "upgrade-insecure-requests": "1",
};

const irctcUserAgent =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36";

module.exports = defineConfig({
  projectId: '7afdkj',

  defaultCommandTimeout: 120000,
  pageLoadTimeout: 120000,
  requestTimeout: 120000,
  responseTimeout: 120000,
  userAgent: irctcUserAgent,
  // video: true,
  env: {
    irctcClientHeaders,
  },

  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
      on("before:browser:launch", (browser = {}, launchOptions) => {
        if (browser.family === "chromium") {
          launchOptions.args.push(`--user-agent=${irctcUserAgent}`);
          launchOptions.args.push("--disable-blink-features=AutomationControlled");
          launchOptions.args.push("--lang=en-IN");
        }

        return launchOptions;
      });

      on('task', {
        log(message) {
          // Then to see the log messages in the terminal
          //   cy.task("log", "my message");
          console.log(message + '\n\n');
          return null;
        },
      });
    },
    chromeWebSecurity: false,
    experimentalModifyObstructiveThirdPartyCode: true
  },
});


