export const FetchFunction = (method, path, body) => {
  const requestOptions = {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include'
  }
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
