from flask import Flask, jsonify, request
import time
import random
from threading import Thread
from flask_socketio import SocketIO  # Replace with your WebSocket library

app = Flask(__name__)
socketio = SocketIO(app)

def generate_event_stream(duration=120, interval=0.5, interrupt_probability=0.1):
  """
  Generates a stream of events with random interrupts and emits them via WebSockets.

  Args:
    - duration: Total time (in seconds) for which the stream will run.
    - interval: Time gap between each event (in seconds).
    - interrupt_probability: Probability of an interrupt occurring (value between 0 and 1).
  """
  start_time = time.time()
  counters = {'A': 1, 'B': 1, 'C': 1, 'D': 1}
  attributes = ['A', 'B', 'C', 'D']

  while time.time() - start_time < duration:
    if random.random() < interrupt_probability:
      # Skip emitting an event
      time.sleep(interval)
      continue

    attribute = random.choice(attributes)
    event = f"{attribute}{counters[attribute]}"
    counters[attribute] += 1

    # Emit the event as JSON via WebSockets
    socketio.emit('event', {'data': event})

    time.sleep(interval)

@app.route('/start_stream', methods=['POST'])
def start_stream():
  data = request.get_json()
  duration = data.get('duration', 60)
  interval = data.get('interval', 0.5)
  interrupt_probability = data.get('interrupt_probability', 0.1)

  # Run the event stream generator in a separate thread
  thread = Thread(target=generate_event_stream, args=(duration, interval, interrupt_probability))
  thread.start()

  return jsonify({"status": "stream started"})

if __name__ == "__main__":
  socketio.run(app, debug=True)
