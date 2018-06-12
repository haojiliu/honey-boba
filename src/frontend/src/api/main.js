import axios from 'axios'

export default {
  getDesigns (cb) {
    console.log('inside vuex api design.getDesigns')
    const path = `http://localhost:5000/api/designs`
    var designsJson = {}
    axios.get(path)
      .then(response => {
        console.log('get response from flask!!!')
        designsJson = response.data
      })
      .catch(error => {
        console.log(error)
      })
    console.log('before calling callback!')
    setTimeout(() => cb(designsJson), 500) // 1 seconds
    console.log('after calling callback!')
  },

  submitReview (cb) {
    console.log('going to submit a review!!')
    const path = `http://localhost:5000/api/review/334823-2343-1324124-2341232`
    axios.post(path, {
      reviewText: 'some review text',
      email: 'some email addr'
    })
      .then(response => {
        console.log(response.data)
      })
      .catch(error => {
        console.log(error)
      })
  }
  // buyProducts (products, cb, errorCb) {
  //   setTimeout(() => {
  //     // simulate random checkout failure.
  //     (Math.random() > 0.5 || navigator.userAgent.indexOf('PhantomJS') > -1)
  //       ? cb()
  //       : errorCb()
  //   }, 100)
  // }
}
