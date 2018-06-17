import axios from 'axios'

export default {
  getDesigns (cb) {
    const path = `http://localhost:5000/api/designs`
    var designsJson = {}
    axios.get(path)
      .then(response => {
        designsJson = response.data
      })
      .catch(error => {
        console.log(error)
      })
    setTimeout(() => cb(designsJson), 500) // 1 seconds
  },

  getOneDesign (cb, uri) {
    const path = `http://localhost:5000/api/design/` + uri
    var designJson = {}
    axios.get(path)
      .then(response => {
        designJson = response.data
      })
      .catch(error => {
        console.log(error)
      })
    setTimeout(() => cb(designJson), 500) // 1 seconds
  },

  refreshOneReview (cb, uri) {
    const path = `http://localhost:5000/api/review/` + uri
    var reviews = []
    axios.get(path)
      .then(response => {
        reviews = response.data
      })
      .catch(error => {
        console.log(error)
      })
    setTimeout(() => cb(reviews), 500) // 1 seconds
  }
}
