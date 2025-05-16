from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(0, 1)

    def on_start(self):

        self.client.post("/login", data={"email": "fake@club.com"})

    @task
    def view_summary(self):
        self.client.get("/showSummary")

    def load_competitions(self):
        with self.client.get("/showSummary", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(
                    f"Temps de chargement trop long : {response.elapsed.total_seconds()}s")
            else:
                response.success()

    @task
    def update_points(self):
        with self.client.post("/purchasePlaces", data={
            "competition": "Fake Competition",
            "club": "Fake Club",
            "places": "1"
        }, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(
                    f"Mise à jour des points trop lente : {response.elapsed.total_seconds()}s")
            else:
                response.success()
