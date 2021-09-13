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

1.	

![](screenshots/screenshot-user-story-1.png "")

    - 


## Python Testing
Custom test cases were written for each application. A total of 65 test were completed. Coverage of 100% was achieved for each application.

### Commissions
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

### Home
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

### Payments
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

### Profiles
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

### Showcase
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
