# honey-boba

# TODOs:
- figure out why server side can't verify a recaptcha response, always return false

- responsive resizing of text
- custom validation message
- report a bug form on /faq page
- show error message when server side failed?

- upload the same file again
- upload the same form again
- upload the same review again
- upload a new file doesn't show up, probably cached somewhere

- implement lazyloading
- move getter methods from logic to model


dribbble:
1, amateur works are deranked to the bottom or not showing up at all.
2. no constructive feedbacks, all compliments
3. no categorization of logo, poster, water color, hand lettering, murals, etc.

my app need to make sure:
1. aiming for students, and amateurs, not professional/good designers
1. amateur/bad designs are not under-represented, they should show up
2. at least half of the comments are constructive feedbacks, not just claps or thumbs ups
3. once you receive enough feedback and are good enough, then you switch to dribbble.

4. make a fun gaming system, where if you reach certain threshold, i give you a badge saying "finally ready for dribbble!!!"
5. mechanism to discourage meaningless thumbups or upvotes, not-so-helpful comments
6. mechanism to force user to form a habit of using it everyday, like, only able to view 25 designs per day

watching top-notch designs doesn't equal being able to create good designs
a design critique platform should be for more than just top notch designs receiving congrats and most of the eyeballs.

## Developers
`npm install -g axios vuejs`
`npm run build`
`python3 web.py`

## Architecture

Majority of the representational code logic has been moved from Flask to Vue on the client side.
Vue router is also used to move the routing to the client side as well.
Flask serves raw data to the front end, mainly piped into Vuex.
