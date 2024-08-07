- receiver <- invoker  <- command <- client
- an object encapsulate all information need to perform an action or trigger an event at a later time.

```javascript
// client side
function main(){
	const bulb = new Bulb();
	const turnOn = new TurnOn(bulb);
	const turnOf = new TurnOff(bulb);

	const remote = new RemoteController();
	remote.execute(turnOn);
	remote.execute(turnOff);
}
```