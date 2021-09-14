# Arts by Bela - Testing Protocol

[Demo of Website](https://arts-by-bela.herokuapp.com/)

Refer to [Main project file](README.md) for further detail.

## Code validation

- [W3C CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/)
- [W3C Markup Validator](https://validator.w3.org/#validate_by_input)
- [JSHint Validator](https://jshint.com/)
- [Python Validator](http://pep8online.com/) 

All CSS, JS and Python files were validated and returned no errors at the time of this entry.
Auto generated Python files, as "app/migrations/*.py" were not validated as they are not created manually.

The HTML templates wer tested by direct input of the rendered website. The errors returned were related to Materialize / Stripe auto generated code. No written custom HTML returned errors. The following templates and scenarios were tested 

- index.html
- showcase.html - with and without artworks on database
- personal_work.html
- profile.html - with and without commissions on database
- new_commission.html
- edit_commission.html
- payment.html 
- payment_success.html
- wip_details.html - as client and as artist with and without wip_illustration/client_comment
- artwork_details.html - as client and as artist with and without final_illustration/client_review
- artwork_details.html - as personal work of artist 

## User stories testing

### As a new visitor to the website,

1. I want to know more about the artist.
![Home Page](screenshots/screenshot-user-story-1.png "Home Page")

    - Loading the home page, the first section has a small introduction about the artist.
2. I want to see previous completed artworks.
![Showcase](screenshots/screenshot-user-story-2.png "Showcase")

    - From the navigation bar, I can load the Showcase page that has examples of the artist's work.
3. I want to read reviews from previous costumers.
![Showcase - Image zoom](screenshots/screenshot-user-story-3.png "Showcase - Image zoom")

    - On the Showcase page, I can click on the image and the client review is displayed.
4. I want to find instructions on how to commission an artwork.
![Home Page - Instructions](screenshots/screenshot-user-story-4.png "Home Page - Instructions")

    - Loading the home page, the second section has the steps on how to commission a new illustration.
5. I want to calculate a quote for the commission.
![Home Page - Quote](screenshots/screenshot-user-story-5.png "Home Page - Quote")

    - Loading the home page, the third section is an interactive quote calculator depending on my illustration requirements.

### As a registered user,

1. I want to request a new commission.
![New Commission](screenshots/screenshot-user-story-6.png "New Commission")

    - Once logged in, I´m redirected to the profile page that has a new commission button. Clicking that button loads the form for me to include my commission request details.
2. I want to pay for the new commission.
![Pay Commission](screenshots/screenshot-user-story-7.png "Pay Commission")

    - By clicking proceed to payment, I can review and pay for my commission by card.
3. I want to be notified as my commission is in progress.
![Email](screenshots/screenshot-user-story-8.png "Email")

    - Once the commission is paid and the artist uploads the illustration, I am notified via email.
4. I want to request changes to the artwork, if necessary.
![WIP details](screenshots/screenshot-user-story-9.png "WIP details")

    - From my profile, I can navigate to the Illustration details and submit comments to the artist.
5. I want to be notified  and download my completed art work.
![Artwork details](screenshots/screenshot-user-story-10.png "Artwork details")

    - Once the artist uploads the illustration, I am notified via email and I can navigate to the illustration details from my profile to download the image.
6. I want access to previous artwork commissions I have ordered, if any.
![Profile](screenshots/screenshot-user-story-11.png "Profile")

    - From my profile, I can see a list of my commissions and redirect to the details page of each commission.
### As the artist,

1. I want to be notified as commissions are requested and commented on.
![Artists emails](screenshots/screenshot-user-story-12.png "Artists emails")

    - As the artist, I receive all emails during the commission workflow.
2. I want to upload the artworks and submit for comments and download.
![Upload images](screenshots/screenshot-user-story-13.png "Upload images")

    - From the commission details page, I can upload the images and submit them to the client.

## Python Testing
Custom test cases were written for each application. A total of 65 test were completed. Coverage of 100% was achieved for each application.

### Commissions
```
Name                                                      Stmts   Miss  Cover
-----------------------------------------------------------------------------
commissions/__init__.py                                       0      0   100%
commissions/admin.py                                         16      0   100%
commissions/apps.py                                           4      0   100%
commissions/context.py                                        6      0   100%
commissions/forms.py                                         25      0   100%
commissions/migrations/0001_initial.py                        5      0   100%
commissions/migrations/0002_auto_20210820_1403.py             4      0   100%
commissions/migrations/0003_auto_20210820_1407.py             4      0   100%
commissions/migrations/0004_size.py                           4      0   100%
commissions/migrations/0005_alter_size_size.py                4      0   100%
commissions/migrations/0006_auto_20210820_1910.py             4      0   100%
commissions/migrations/0007_commission.py                     5      0   100%
commissions/migrations/0008_auto_20210902_1145.py             4      0   100%
commissions/migrations/0009_auto_20210904_1240.py             6      0   100%
commissions/migrations/0010_alter_wip_client_comment.py       4      0   100%
commissions/migrations/0011_artwork.py                        5      0   100%
commissions/migrations/0012_auto_20210913_1019.py             4      0   100%
commissions/migrations/__init__.py                            0      0   100%
commissions/models.py                                        96      0   100%
commissions/templatetags/split_filter.py                      5      0   100%
commissions/testsModels.py                                   79      0   100%
commissions/testsViews.py                                   399      0   100%
commissions/urls.py                                           3      0   100%
commissions/views.py                                        166      0   100%
-----------------------------------------------------------------------------
TOTAL                                                       852      0   100%
```

### Home
```
Name                          Stmts   Miss  Cover
-------------------------------------------------
home/__init__.py                  0      0   100%
home/apps.py                      4      0   100%
home/migrations/__init__.py       0      0   100%
home/tests.py                     6      0   100%
home/urls.py                      3      0   100%
home/views.py                     7      0   100%
-------------------------------------------------
TOTAL                            20      0   100%
```

### Payments
```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
payments/__init__.py                  0      0   100%
payments/apps.py                      4      0   100%
payments/migrations/__init__.py       0      0   100%
payments/tests.py                    53      0   100%
payments/urls.py                      3      0   100%
payments/views.py                    46      0   100%
-----------------------------------------------------
TOTAL                               106      0   100%
```

### Profiles
```
Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
profiles/__init__.py                                 0      0   100%
profiles/admin.py                                    5      0   100%
profiles/apps.py                                     4      0   100%
profiles/forms.py                                   11      0   100%
profiles/migrations/0001_initial.py                  7      0   100%
profiles/migrations/0002_auto_20210913_1019.py       4      0   100%
profiles/migrations/__init__.py                      0      0   100%
profiles/models.py                                  15      0   100%
profiles/tests.py                                   54      0   100%
profiles/urls.py                                     3      0   100%
profiles/views.py                                   22      0   100%
--------------------------------------------------------------------
TOTAL                                              125      0   100%
```

### Showcase
```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
showcase/__init__.py                  0      0   100%
showcase/apps.py                      4      0   100%
showcase/forms.py                     8      0   100%
showcase/migrations/__init__.py       0      0   100%
showcase/tests.py                    50      0   100%
showcase/urls.py                      3      0   100%
showcase/views.py                    38      0   100%
-----------------------------------------------------
TOTAL                               103      0   100%
```

## Manual testing of features

The deployed Heroku website was viewed on  desktops screens (21 and 13 inches) and also on Motorola G6 Play device.

<!-- The website was tested with Google Chrome (v.91.0), Mozilla Firefox (v.89) and Microsoft Edge (v.91) browsers.

On mobile, it was viewed with Google Chrome application v.91.0 on Android 9.

The Developer Tools of Google Chrome (v.91) on desktop was used to verify responsiveness on different devices. -->

1. **Home Page**:

   | Test No. | Action & expected results                                    | Pass / Fail |
   | -------- | :----------------------------------------------------------- | :---------- |
   | 1.1      |     |       |


   ### Known issues
- The files are only open on a new tab, instead of downloaded from the S3 bucket on the deployed enviroment. To fix this issue, the Content-Disposition of the file has to be set at custom storage classes. This was not implemented to avoid data tranfer fees. For further information, refer to [StackOverflow](https://stackoverflow.com/questions/43208401/add-dynamic-content-disposition-for-file-namesamazon-s3-in-python).