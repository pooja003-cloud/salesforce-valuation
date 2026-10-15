# The project in plain English

## The one-line version

Buying a share is buying a small piece of a business. This project works out whether one share of Salesforce is a fair price for the money that business will make over time. The answer: it's worth about $230, almost exactly the $236 it trades at.

## Whose question is this?

A regular long-term investor's: someone buying a few shares and holding them. Not a company trying to buy all of Salesforce (they would pay more), not a short-term trader (they care about next month's price moves), and not a lender (they only care about getting repaid).

## Why this project

Lots of people invest, but few can explain *why* a stock is worth what it costs. Professional investors answer that with a financial model: predict how much cash a company will make, then work out what that future cash is worth today. This project does that for a real company, using its official reports, instead of a textbook example.

## Why Salesforce

Salesforce makes software that businesses use to manage their customers, sold on subscription, like Netflix but for companies.

- **Much of its future income is already promised.** Customers sign long contracts, often paying upfront. It's like a landlord with tenants on multi-year leases: next year's rent is fairly predictable.
- **It's big and well documented,** so the information is reliable.
- **It's at an interesting moment.** It's betting heavily on AI and just borrowed a lot of money to buy back its own shares.

## How it works: the rental-property version

1. **Estimate the rent you'll collect.** For Salesforce, that's subscription sales, based on contracts already signed.
2. **Subtract running costs:** staff, marketing, taxes. What's left is the cash the business actually produces.
3. **Money later is worth less than money now.** £100 in five years is worth less than £100 today, because today's money could be earning a safe return elsewhere. So future cash is scaled down to today's value.
4. **Add it up, subtract what the company owes, divide by the number of shares.** That's a fair price per share.

## Three versions of the future

| Story | What happens | Fair price |
|---|---|---:|
| Gloomy | Growth slows, AI costs eat into profits | ~$180 |
| Middle | Roughly what the company itself expects | ~$230 |
| Optimistic | Its AI products take off | ~$265 |

The actual price, $236, sits right in the middle, so the market is betting on the middle story.

## What I learned

- **A share price is a bet on the future.** It only makes sense once you spell out what you're assuming about growth and costs.
- **Small assumptions matter a lot.** Change the return you expect by one percentage point and fair value moves by roughly $10–20 a share.
- **Interest rates affect every investment.** Safe government bonds pay over 5% right now, so investors demand more from riskier things like tech stocks, which pulls their fair value down.
- **How a company pays its staff matters.** Salesforce pays a large part of salaries in shares. Ignoring that cost would make the company look about 20% more valuable.
- **"Fair price" is a valid answer.** Not every analysis ends in "buy". Knowing what not to overpay for is useful too.

## The outcome

1. A full model that turns Salesforce's real financial reports into a fair value per share.
2. A clear conclusion: worth about $230, roughly what it costs. Buying only makes sense if you believe its AI push will beat expectations.
3. Three scenarios and sensitivity tables showing how the answer changes when assumptions change.
