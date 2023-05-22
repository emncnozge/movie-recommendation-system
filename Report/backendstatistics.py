import requests
import time
import matplotlib.pyplot as plt

url = "http://127.0.0.1:8000/Search?search=Cinderella's&adult=0"
amount_of_requests = 50


response_times = []
availability = []

for _ in range(amount_of_requests):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    response_time = end_time - start_time
    response_times.append(response_time)

    if response.status_code == 200:
        availability.append(1)
    else:
        availability.append(0)

average_response_time = sum(response_times) / len(response_times)
average_availability = sum(availability) / len(availability) * 100

# Calculate upper limit for y-axis with 0.2 seconds buffer
max_response_time = max(response_times)
min_response_time = min(response_times)
y_upper_limit = max_response_time + 0.001
y_lower_limit = max(min_response_time - 0.001, 0)

# Plotting the response times with improved aesthetics
plt.figure(figsize=(12, 5))
plt.plot(response_times, marker='o', linestyle='-', color='b')
plt.xlabel('İstek')
plt.ylabel('Yanıt süresi (saniye)')
plt.title('Film Arama API | {} İstek İçin Yanıt Süresi'.format(
    amount_of_requests))
plt.grid(True)
plt.xticks(range(amount_of_requests), range(1, amount_of_requests + 1))
plt.ylim(y_lower_limit, y_upper_limit)
plt.tight_layout()

# Saving the plot with higher resolution
plt.savefig('Search Request.png', dpi=600)

print('Average Response Time: {:.4f} seconds'.format(average_response_time))
