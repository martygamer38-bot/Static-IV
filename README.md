# Smart Data Company Announcements (GitHub version)

Press **Today's announcements** to see the day's UK Smart Data company news. Use the calendar for any day, and **This month** for the monthly roll-up.

## Set up once
1. Delete everything in the repo, then upload everything in this zip, including the hidden `.github` folder. Everything except `.github` sits at the top level.
2. Go to Settings > Actions > General > Workflow permissions, choose **Read and write permissions** and save.
3. Go to Settings > Pages and set the source to `main` branch, `/ (root)`.
4. Press **Refresh now** on the page, then **Run workflow** on GitHub. Results show in about 3 minutes.

After that it updates by itself at 6am, 9am, 12pm, 3pm and 6pm (UK winter time) on weekdays, and at 9am at weekends.

## Optional: automatic company details
Get a free API key from the Companies House developer hub. Add it under Settings > Secrets and variables > Actions > New repository secret, with the name `COMPANIES_HOUSE_API_KEY`. HQ, what the company does and size then fill in automatically.
