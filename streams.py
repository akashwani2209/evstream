import time
import random

def generate_event_stream(duration=60, interval=0.5, interrupt_probability=0.01):
    """
    Generates a stream of events with random interrupts.
    
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
            # Skip emitting an event to simulate an interrupt
            time.sleep(interval)
            continue

        attribute = random.choice(attributes)
        event = f"{attribute}{counters[attribute]}"
        print(event)
        counters[attribute] += 1
        time.sleep(interval)

if __name__ == "__main__":
    generate_event_stream()


# Server (Events TOPIC_NAME(RANDOM))
# Client (Listener) 

# Event stream: Redis, Kafka