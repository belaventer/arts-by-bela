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
