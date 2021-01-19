from examples.inversion_of_control_2.inner.service import Service
from examples.inversion_of_control_2.outer.repository import Repository

if __name__ == "__main__":
    service = Service(repository=Repository())
    print(service())
