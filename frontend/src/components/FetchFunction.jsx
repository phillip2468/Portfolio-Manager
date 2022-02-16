export const FetchFunction = (method, path, body) => {
  const requestOptions = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-TOKEN': getCookie('csrf_access_token')[0]
    },
    credentials: 'include'
  }

  console.log(requestOptions)
  if (body !== null) {
    requestOptions.body = JSON.stringify(body)
  }

  return new Promise((resolve, reject) => {
    fetch(`${path}`, requestOptions)
      .then(response => {
        if (response.status !== 200) {
          response.json().then((error) => {
            reject(error.error)
          })
        } else {
          response.json().then((data) => {
            resolve(data)
          })
        }
      })
      .catch((error) => {
        console.log(error)
      })
  })
}

function getCookie (name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';')
}
