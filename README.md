# AnonBeta

# Create prod docker image:
docker-compose build prod --no-cache
docker tag honey-boba_app:latest divid86391/design-review:latest
docker push divid86391/design-review

# Create dev docker image:
docker-compose build dev
docker-compose up -d dev

# AWS Deploy steps:
- launch an instance
- install docker
- sudo docker login
- sudo docker pull divid86391/design-review:latest
- sudo docker run -d -p 80:80 -p 9002:9002 --v /tmp:/srv/vol --name app divid86391/design-review:0.2a

- sudo docker run -d -p 5000:5000 -p 9002:9002 --name app honey-boba_dev:latest

- scp -i ~/src/haoji_liu_personal.pem app_prod.db ubuntu@34.201.36.179:/tmp/
app_prod.db                      

# TODOs before release:

- set up dev vs prod global vars
- enable google analytics
- timezone should change according to client side timezone
- remove console prints on the front end

# TODOs after release:
- move thumbnails and original images to s3
- move database write out into a volume
- move to https

- switch to nginx and uwsgi

- switch from using User.id to User.uid
- research on how cookie or token can be used to remember some info like "auth'd on this computer already, or submitted XYZ on this computer..."
- custom validation message
- show error message when server side code failed?
- upload the same file again
- upload the same form again
- upload the same review again

- make a logo

- log rotation

- drag and drop instead of a CHOOSE FILE button
- implement lazyloading
- implement masonry style
- implement tags, filter/search
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
