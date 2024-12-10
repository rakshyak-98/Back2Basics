[getting-started/media-devices](https://webrtc.org/getting-started/media-devices)

```js
navigator.mediaDevices.getUserMedia({vide: true, audio: true})
	.then( stream => {
		console.log("Got MediaStream: ", stream)
	})
```
- will trigger a permissions request. If the user accepts the permission, the promise is resolved with a `MediaStream` containing one video and one audio track. If the permission is denied, a `PermissionDenied Error` is thrown. In case there are no matching devices connected, a `NotFoundError` will be thrown.

## Querying media devices
- in more complex application, we will likely want to check all the connected cameras and microphones and provide the appropriate feedback to the user.
```js
function getConnectedDevices(type, callback){
	navigator.mediaDevices.enumerateDevices().then(devices => {
		const filtered = devices.filter(device => device.kind === type);
		callback(filtered);
	})
}

getConnectedDevices('videoinput', cameras => console.log("Cameras found", cameras));
```

## Listening for devices changes
- most computers support plugging in various devices during runtime. It could be a webcam connected by USB, a Bluetooth headset, or a set of external speakers. In order to properly support this, a web application should listen for the changes of media devices.

> [!INFO] this is done by adding a listener to `navigator.mediaDevices` for the `devicechange` event.

```js
function updateCameraList(cameras) {
	const listElement = document.querySelector('select#availableCameras")
	 listElement.innerHTML = '';
	 cameras.map(camera => {
		 const cameraOption = document.createElement('option');
		 cameraOption.label = camera.label;
		 cameraOption.value = camera.deviceId;
	 }).forEach(cameraOption => listElement.add(camerOption));
}

async function getConnectedDevices(type){
	const devices = await navigator.mediaDevices.enumerateDevices();
	return devices.filter(device => device.kind === type);
}

const videoCameras = getConnectedDevices('videoinput');
updateCameraList(videoCameras);
navigator.mediaDevices.addEventListener('devicechange', event => {
	const newCameraList = getConnectedDevices('video');
	updateCameraList(newCameraList);
})
```

## Media constraints

> [!NOTE] it is recommended that applications that use the `getUserMedia()` API first check the existing devices and then specifies a constraint that matches the exact device using the `deviceId` constraint.
- we can enable echo cancellation on microphones or set a specific or minimum width and height of the video from the camera.

```js
async function getConnectedDevices(type) {
	const devices = await navigator.mediaDevices.enumerateDevices();
	return devices.filter(device => device.kind === type);
}

async function openCamera(cameraId, minWidth, minHeight){
	const constraints = {
		'audio': {'echoCancallation': true},
		'video': {
			'deviceId': cameraId;
			'width': {'min': minWidth},
			'height': {'min': minHeight}
		}
	}
	return await navigator.mediaDevices.getUserMedia(constraints);
}

const cameras = getConnectedDevices('videoinput')
if(cameras && cameras.length > 0){
	const stream = openCamera(cameras[0].deviceId, 1280, 720);
}
```

## Local playback

- Once a media device has opened we have a `MediaStream` available, we can assign it to a video or audio element to play the stream locally.

```js
async function playVideoFromCamers(){
	try{
		const constraints = {'video': true, 'audio': true}
		const stream = await navigator.mediaDevices.getUserMedia(constraints);
		const videoElement = document.querySelector('video#localVideo');
		videoElement.srcObject = stream;
	}catch(error) {
		console.error('Error opening video camera.', error)
	}
}
```

