# honey-boba

# TODOs before release:
- switch from using User.id to User.uid
- disable buttons if email not confirmed
- move email confirmation widget and design info updater widget out of Uploaded.vue
- each design has a field that designer can add like "I want to know which font fits more, etc.", display the field under each design
- navbar drop down doesn't work

- tweak email template
- tweak UI

- make a docker image and upload to docker cloud
- register a domain name
- register an email
- deploy to aws

- make a logo


# TODOs after release:
- research on how cookie or token can be used to remember some info like "auth'd on this computer already, or submitted XYZ on this computer..."
- custom validation message
- show error message when server side code failed?
- responsive resizing of text
- upload the same file again
- upload the same form again
- upload the same review again

- log rotation

- drag and drop instead of a CHOOSE FILE button
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
