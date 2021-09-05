# Arts by Bela

![Arts by Bela Website](# "Arts by Bela")

[Demo of Website](#)

Arts by Bela is the website for the digital illustrator Bela where users can request commissions, interact, pay and leave reviews for the artist.

## UX

### User stories

As a new visitor to the website,

1. I want to know more about the artist.
2. I want to see previous completed artworks.
3. I want to read reviews from previous costumers.
4. I want to find instructions on how to commission an artwork.
5. I want to calculate a quote for the commission.

As a registered user,

1. I want to request a new commission.
2. I want to pay for the new commission.
3. I want to be notified as my commission is in progress.
4. I want to request changes to the artwork, if necessary.
5. I want to accept and download my completed art work.
6. I want access to previous artwork commissions I have ordered, if any.

As the artist,

1. I want to be notified as commissions are requested, accepted or rejected.
2. I want to upload the artworks and submit for acceptance or comments.

### Strategy 

The main user goal for the client is to order, pay for and receive completed art concepts as requested.
The main user goal to the artist is to have an easy platform to communicate with the clients and automatically update its own portfolio.


### Scope

The main features for the website is a landing home page with simple *About me* and information on how to commission a concept/illustration and a quote calculator, a *Art Showcase* and a *Register / Login* pages.

For Registered users, the landing page is the *Profile* where it will have options to see the previous and current orders as well as make new ones.

The Artist will have it's own *Profile* page with view of all completed and current orders.

**Future scope**:
	- Booking system to avoid having to many open commissions at one given time, causing delay and frustration to clients.
	- A live message chat for each open commission.

### Structure

The website will have a responsive grid system applied through the pages with a side nav-bar.

The *Showcase* page will display all completed commissions that will expand on mouse hover. On mobile, the page will be a carousel.

#### Apps Structure

The website will be broken in 5 different apps:
	- Home: the app will handle the home page and quote calculator.
	- Showcase: the app will handle the showcase page. It will communicate with the Commissions app models.
	- Commissions: the app will handle all new, active and completed commissions.
	- Payment: the app will handle payment for new commissions.
	- Profiles: the app will handle all profiles.

#### Database Structure

The entity relational diagram and overall workflow can be found in [ERD](ERD.pdf "Arts by Bela ERD").

### Skeleton

- [Wireframes](wireframes.jpg "Arts by Bela Wireframes")

#### Deviation from layout

- The Home button will be available for authenticated users as the instructions and quote calculator are referred on the  home page.

### Surface

#### Colour

The website will use a monochrome colours not to offset the existing artworks. 

#### Typography

The typography will be round and soft using the combinations of fonts Nunito and Montsserat .


## Features

The website is consistent of:

- **Base layout:** responsive layout that holds the navigation links and copyright.
- **Home page:** Simple page with static information about the artist and how to commission an artwork. On the bottom of the page, there is a interactive calculator for quoting the commission price, given the requirements.
- **User Authentication:** The user authentication is given by [django-allauth](https://django-allauth.readthedocs.io/en/latest/index.html). The form fields are dynamically updated to match the rest of the website layout.

### Existing Features

**Navigation Bar**: The responsive navigation bar is fixed to the right of the screen on desktop views and collapsed static at the top of the screen for tablet/mobile. The navigation links depend on user authentication.

**Quote Calculator:** Simple script that returns the quote value given the Size, Resolution and Number of Characters specified. The quote is update on the change of each value.

**User Authentication Layout:** All django-allauth templates are update with materialize classes as the document loads to match website layout.

### Features left to implement



## Technologies used

### Languages

- HTML | HTML5
- CSS | CSS3
- JavaScript | JS ES6
- Python | Python3

### Libraries, Frameworks & Programs

- [Gitpod](https://gitpod.io/workspaces/):
  The developer used Gitpod as the IDE for building the website.

- [Heroku](https://www.heroku.com/):
  Used for application deployment.

- [Django](https://www.djangoproject.com/):
  Used for application development.

- [Materialize](https://materializecss.com/):
  Used for general styling.

- [Typora](https://typora.io/#):
  Used for Markdown editing of README and TESTING files.

- [Clip Studio Paint](https://www.clipstudio.net/en/):
  Used for logo editing.

- [AutoPrefixer](https://autoprefixer.github.io):
  Used on CSS to ensure functionality across browsers.

- [jQuery API](https://api.jquery.com/):
  Used for custom JavaScript code.

## Testing

Refer to [TESTING.md](TESTING.md) file for testing details.

## Deployment

This project was developed using the Gitpod IDE, committed to git and pushed to GitHub.

### Deploy to Heroku from GitHub Repository:

- Log in to [Heroku](https://id.heroku.com/login).
- Create a new application with unique name and setting the region.
- Under Deploy tab, select GitHub as the Deployment Method.
- Search for the GitHub repository and click Connect.
- Under Settings tab, click "Reveal Config Vars"
- Include the environment  private variables and values:
  - STRIPE_SECRET_KEY
  - STRIPE_PUBLIC_KEY

- Under Deploy tab, choose the branch and click Enable Automatic Deploys in the Automatic Deploys section.

Note: ensure you have a Procfile and requirements.txt indicating language and packs required to run the application on your repository.

### Download project to local IDE:

- Navigate to [GitHub Repository](#).
- Click in Code and choose the local download method:
  - ZIP file - unpack - run on local IDE
  - Copy Git URL - open IDE terminal - run git clone
- A clone of the project is now available on your machine.

Note: ensure you have the configuration variables defined in the IDE environment for the project and the you install the requirements for the application.

`- pip install -r requirements.txt`

### Fork project:

- Navigate to [GitHub Repository](#).
- Click in Fork. A duplicate repo will be created for your user.

Further information on [GitHub Docs](https://docs.github.com/en).

## Credit

### Content

All content was created by the developer.

### Media

All original media was created by the developer with [Clip Studio Paint](https://www.clipstudio.net/en/) as recreational art.

References media used on orders to demonstrate features listed below:

### Code

Favicon added as per ["Add A Favicon to A Website in HTML | Learn HTML and CSS | HTML Tutorial | HTML for Beginners"](https://www.youtube.com/watch?v=kEf1xSwX5D8) by Dani Krossing.

Create file preview from file input solution found in [StackOverflow](https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded).

Custom Split Filter from [StackOverflow](https://stackoverflow.com/questions/41932634/how-to-split-the-string-in-django-template).

[W3Schools](https://www.w3schools.com/) was referenced throughout the project for HTML, CSS and Python references.

[jQuery Documentation](https://api.jquery.com/) was referenced throughout the project for jQuery references.

[Django](https://docs.djangoproject.com/en/3.2/) documentation was referenced throughout the project for Django references.

### Acknowledgment

I would like to thank my mentor Gerry McBride for insightful tips and suggestions. 

## Disclaimer

This project purpose is only educational.