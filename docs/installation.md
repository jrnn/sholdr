Installation
------------
- Assumption is you're on Linux. If not, you'll have to figure this out yourself.

### Locally
1. Open command line and navigate to an appropriate folder.
2. Clone the project from GitHub:
        ```
        git clone git@github.com:jrnn/sholdr.git
        ```
3. Open root folder:
        ```
        cd sholdr
        ```
4. Create and activate Python virtual environment:
        ```
        python3 -m venv venv
        source venv/bin/activate
        ```
5. Upgrade pip (optional) and install needed dependencies:
        ```
        pip install --upgrade pip
        pip install -r requirements.txt
        ```
6. Run sholdr locally:
        ```
        python3 run.py
        ```
7. Open http://127.0.0.1:5000/ in a browser.

### On Heroku
0. Have sholdr running locally, as advised above.
1. Make sure you have Heroku account and Heroku CLI installed, e.g. check:
        ```
        heroku --version
        ```
2. Make sure you're in the project's root folder (see above).
3. Create heroku app:
        ```
        heroku create unique-app-name-goes-here
        ```
   ...where, obviously, you pick whatever app name you like.
4. Add Heroku Postgres (free hobby-dev plan):
        ```
        heroku addons:add heroku-postgresql:hobby-dev
        ```
5. Set environment variables:
   - 'HEROKU' = 1. This is only to let the app know it's running on Heroku.
   - 'SECRET_KEY' = ... Use whatever random sequence of characters and numbers
     you like. For instance, generate a UUID.
   - 'MAX_SHARES' = ... Optional. You can set an upper bound on how many shares
     can be issued. This is a useful safeguard when running a hobby DB with very
     limited storage.
        ```
        heroku config:set HEROKU=1
        heroku config:set SECRET_KEY=RandomSequenceOfCharsAndNumb3r5
        heroku config:set MAX_SHARES=666
        ```
6. Deploy project to heroku:
        ```
        git remote add heroku https://git.heroku.com/unique-app-name-goes-here.git
        git add .
        git commit -m "hello heroku"
        git push heroku master
        ```
7. Application should now run in https://unique-app-name-goes-here.herokuapp.com/
8. If you want to develop sholdr (i.e. will do changes to the source code), it's
   a good idea to enable Heroku—GitHub integration and automatic deployments, as
   per Heroku's [excellent instructions](https://devcenter.heroku.com/articles/github-integration)
9. Though there's a .travis.yml, disregard it. Since there's zero tests, no
   point in hooking up CI.
