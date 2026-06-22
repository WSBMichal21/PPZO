from abc import ABC, abstractmethod


class Rentable(ABC):
    @property
    @abstractmethod
    def is_available(self):
        pass

    @abstractmethod
    def rent(self):
        pass

    @abstractmethod
    def return_vehicle(self):
        pass


class Vehicle(Rentable):
    def __init__(self, vehicle_id, brand, model, hourly_rate):
        if not vehicle_id:
            raise ValueError("Identyfikator pojazdu nie może być pusty.")
        if not brand:
            raise ValueError("Marka pojazdu nie może być pusta.")
        if not model:
            raise ValueError("Model pojazdu nie może być pusty.")
        if hourly_rate <= 0:
            raise ValueError("Stawka godzinowa musi być większa od zera.")

        self._id = vehicle_id
        self._brand = brand
        self._model = model
        self._hourly_rate = hourly_rate
        self._is_available = True

    @property
    def id(self):
        return self._id

    @property
    def brand(self):
        return self._brand

    @property
    def model(self):
        return self._model

    @property
    def hourly_rate(self):
        return self._hourly_rate

    @property
    def is_available(self):
        return self._is_available

    def rent(self):
        if not self._is_available:
            raise ValueError("Pojazd jest już wypożyczony.")
        self._is_available = False

    def return_vehicle(self):
        self._is_available = True

    def calculate_cost(self, hours):
        if hours <= 0:
            raise ValueError("Liczba godzin musi być większa od zera.")
        return self._hourly_rate * hours

    @abstractmethod
    def get_description(self):
        pass


class Car(Vehicle):
    def __init__(self, vehicle_id, brand, model, hourly_rate, seats, has_air_conditioning):
        super().__init__(vehicle_id, brand, model, hourly_rate)

        if seats < 2:
            raise ValueError("Samochód musi mieć minimum 2 miejsca.")

        self._seats = seats
        self._has_air_conditioning = has_air_conditioning

    @property
    def seats(self):
        return self._seats

    @property
    def has_air_conditioning(self):
        return self._has_air_conditioning

    def calculate_cost(self, hours):
        cost = super().calculate_cost(hours)

        if self._has_air_conditioning:
            cost += 20

        return cost

    def get_description(self):
        air_conditioning = "tak" if self._has_air_conditioning else "nie"
        return f"Samochód: {self.brand} {self.model}, id: {self.id}, miejsca: {self.seats}, klimatyzacja: {air_conditioning}, dostępny: {self.is_available}"


class Bike(Vehicle):
    def __init__(self, vehicle_id, brand, model, hourly_rate, is_electric):
        super().__init__(vehicle_id, brand, model, hourly_rate)
        self._is_electric = is_electric

    @property
    def is_electric(self):
        return self._is_electric

    def calculate_cost(self, hours):
        cost = super().calculate_cost(hours)

        if self._is_electric:
            cost *= 1.2

        return cost

    def get_description(self):
        bike_type = "elektryczny" if self._is_electric else "standardowy"
        return f"Rower {bike_type}: {self.brand} {self.model}, id: {self.id}, dostępny: {self.is_available}"


class Customer:
    def __init__(self, customer_id, full_name):
        if not customer_id:
            raise ValueError("Identyfikator klienta nie może być pusty.")
        if not full_name:
            raise ValueError("Imię i nazwisko klienta nie może być puste.")

        self._id = customer_id
        self._full_name = full_name
        self._rentals = []

    @property
    def id(self):
        return self._id

    @property
    def full_name(self):
        return self._full_name

    @property
    def rentals(self):
        return tuple(self._rentals)

    def change_name(self, new_full_name):
        if not new_full_name:
            raise ValueError("Nowe imię i nazwisko nie może być puste.")

        self._full_name = new_full_name

    def add_rental(self, rental):
        self._rentals.append(rental)

    def __str__(self):
        return f"Klient: {self.full_name}, id: {self.id}, liczba wypożyczeń: {len(self._rentals)}"


class Rental:
    def __init__(self, rental_id, customer, vehicle, hours):
        if not rental_id:
            raise ValueError("Identyfikator wypożyczenia nie może być pusty.")
        if hours <= 0:
            raise ValueError("Liczba godzin musi być większa od zera.")

        self._id = rental_id
        self._customer = customer
        self._vehicle = vehicle
        self._hours = hours
        self._total_cost = vehicle.calculate_cost(hours)
        self._is_finished = False

        self._vehicle.rent()

    @property
    def id(self):
        return self._id

    @property
    def customer(self):
        return self._customer

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def hours(self):
        return self._hours

    @property
    def total_cost(self):
        return self._total_cost

    @property
    def is_finished(self):
        return self._is_finished

    def finish(self):
        if self._is_finished:
            raise ValueError("Wypożyczenie zostało już zakończone.")

        self._is_finished = True
        self._vehicle.return_vehicle()

    def __str__(self):
        status = "zakończone" if self._is_finished else "aktywne"
        return f"Wypożyczenie: {self.id}, klient: {self.customer.full_name}, pojazd: {self.vehicle.brand} {self.vehicle.model}, czas: {self.hours} h, koszt: {self.total_cost:.2f} zł, status: {status}"


class RentalService:
    def __init__(self):
        self._vehicles = []
        self._customers = []
        self._rentals = []

    @property
    def vehicles(self):
        return tuple(self._vehicles)

    @property
    def customers(self):
        return tuple(self._customers)

    @property
    def rentals(self):
        return tuple(self._rentals)

    def add_vehicle(self, vehicle):
        if any(v.id == vehicle.id for v in self._vehicles):
            raise ValueError("Pojazd o takim identyfikatorze już istnieje.")

        self._vehicles.append(vehicle)

    def add_customer(self, customer):
        if any(c.id == customer.id for c in self._customers):
            raise ValueError("Klient o takim identyfikatorze już istnieje.")

        self._customers.append(customer)

    def create_rental(self, customer_id, vehicle_id, hours):
        customer = self._find_customer_by_id(customer_id)
        vehicle = self._find_vehicle_by_id(vehicle_id)

        if not vehicle.is_available:
            raise ValueError("Wybrany pojazd nie jest dostępny.")

        rental_id = f"R-{len(self._rentals) + 1:03}"
        rental = Rental(rental_id, customer, vehicle, hours)

        self._rentals.append(rental)
        customer.add_rental(rental)

        return rental

    def finish_rental(self, rental_id):
        rental = self._find_rental_by_id(rental_id)
        rental.finish()

    def _find_customer_by_id(self, customer_id):
        for customer in self._customers:
            if customer.id == customer_id:
                return customer

        raise ValueError("Nie znaleziono klienta.")

    def _find_vehicle_by_id(self, vehicle_id):
        for vehicle in self._vehicles:
            if vehicle.id == vehicle_id:
                return vehicle

        raise ValueError("Nie znaleziono pojazdu.")

    def _find_rental_by_id(self, rental_id):
        for rental in self._rentals:
            if rental.id == rental_id:
                return rental

        raise ValueError("Nie znaleziono wypożyczenia.")


def main():
    rental_service = RentalService()

    car = Car("CAR-001", "Toyota", "Corolla", 50, 5, True)
    bike = Bike("BIKE-001", "Kross", "Level", 20, False)
    electric_bike = Bike("BIKE-002", "Giant", "E-Tour", 35, True)

    customer = Customer("C-001", "Jan Kowalski")

    rental_service.add_vehicle(car)
    rental_service.add_vehicle(bike)
    rental_service.add_vehicle(electric_bike)
    rental_service.add_customer(customer)

    print("=== Lista pojazdów ===")

    for vehicle in rental_service.vehicles:
        print(vehicle.get_description())

    print()
    print("=== Polimorfizm: koszt wypożyczenia na 3 godziny ===")

    for vehicle in rental_service.vehicles:
        print(f"{vehicle.id}: {vehicle.calculate_cost(3):.2f} zł")

    print()
    print("=== Utworzenie wypożyczenia ===")

    rental = rental_service.create_rental("C-001", "CAR-001", 4)
    print(rental)

    print()
    print("=== Dostępność pojazdów po wypożyczeniu ===")

    for vehicle in rental_service.vehicles:
        print(vehicle.get_description())

    print()
    print("=== Zakończenie wypożyczenia ===")

    rental_service.finish_rental(rental.id)
    print(rental)

    print()
    print("=== Historia klienta ===")
    print(customer)

    for customer_rental in customer.rentals:
        print(customer_rental)


if __name__ == "__main__":
    main()
