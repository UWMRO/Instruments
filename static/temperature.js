function initializeTemperatureControls() {
  /* Every HTML element has an equivalent object we can use via JavaScript. The global variable "document" is a virtual
     element that contains all of the elements inside of the HTML content shown in the browser. The function
     "getElementById" lets us find the element inside the document with a specific id. For example, the next line
     will give us an object corresponding to the HTML element <button id="temperature-refresh"...
   */
  const refreshButton = document.getElementById('temperature-refresh')
  const temperatureDisplay = document.getElementById('temperature-display')
  // This creates a new function that the browser will call any time the user clicks the refresh button.
  refreshButton.addEventListener('click', async () => {
    // this grays out the button and makes it unclickable
    refreshButton.disabled = true
    temperatureDisplay.innerText = 'loading...'
    try {
      /* fetch() is a global function that makes a HTTP request. Here we make a GET request (the default type of
         request) to the path "/temperature" on the same server that gave us the HTML page. We use the "await" keyword
         to say "we know that fetch() makes a network request and won't give us results instantly, so pause the rest
         of this JavaScript function until we get a response". The result of awaiting fetch() is an object with metadata
         about our request, but in order to get the actual contents we need to await another function json() that will
         read the results and convert them into a JavaScript object.
       */
      const result = await (await fetch('/temperature')).json()
      temperatureDisplay.innerText = JSON.stringify(result, null, 2)
      // equivalent to this Python:
      // for sourceName, value in result['temperatures'].items()
      Object.entries(result.temperatures).forEach((sourceName, value) => {
        const htmlElement = document.getElementById(`temperature-value-${sourceName}`)
        if(htmlElement) {
          htmlElement.innerText = value
        }
      })
    } catch(e) {
      /* Either fetch() or json() might throw an error, e.g. if the network request fails or the response is in an
         unexpected format.
       */
      console.log(e)
      temperatureDisplay.innerText = "An error occurred when getting the camera's temperature. Consult your browser's debug console for details."
    } finally {
      // regardless of whether we succeeded or not, we want to make the button clickable again
      refreshButton.disabled = false
    }
  })
}

/* This script may load before all of the HTML elements do. We know that the elements will be available when the
   the document's ready state is "complete", so we register for changes in ready state and check on each change.
 */
document.addEventListener('readystatechange', () => {
  if(document.readyState === 'complete') {
    initializeTemperatureControls()
  }
})
