from abc import ABC, abstractmethod

# ==========================================
# 1. DATA ENTITIES & OOP STRUCTURE
# ==========================================

class Learner:
    """Class representing a student/learner."""
    def __init__(self, learner_id, name):
        self.learner_id = learner_id
        self.name = name

    def __str__(self):
        return f"{self.name} (ID: {self.learner_id})"


# ABSTRACT SUPERCLASS
class TransportVehicle(ABC):
    """Abstract superclass for all transport vehicles."""
    def __init__(self, vehicle_id, capacity):
        self.vehicle_id = vehicle_id
        self.capacity = capacity
        self.passengers = []  # List to hold Learner objects

    # Polymorphic method to be implemented by subclasses
    @abstractmethod
    def calculate_operating_cost(self, route_distance):
        pass

    def is_full(self):
        return len(self.passengers) >= self.capacity

    def add_passenger(self, learner):
        if not self.is_full():
            self.passengers.append(learner)
            return True
        return False

    def remove_passenger(self, learner_id):
        for passenger in self.passengers:
            if passenger.learner_id == learner_id:
                self.passengers.remove(passenger)
                return True
        return False


# SUBCLASSES
class Bus(TransportVehicle):
    """Large capacity, higher base cost but lower per-km cost."""
    def calculate_operating_cost(self, route_distance):
        base_cost = 50.0
        return base_cost + (1.5 * route_distance)

class Minibus(TransportVehicle):
    """Medium capacity, balanced costs."""
    def calculate_operating_cost(self, route_distance):
        base_cost = 30.0
        return base_cost + (2.0 * route_distance)

class Van(TransportVehicle):
    """Low capacity, lowest base cost but high per-km cost."""
    def calculate_operating_cost(self, route_distance):
        base_cost = 15.0
        return base_cost + (2.5 * route_distance)


class Route:
    """Class representing a transport route."""
    def __init__(self, route_id, name, distance):
        self.route_id = route_id
        self.name = name
        self.distance = distance
        self.vehicles = {} # Dictionary of vehicles assigned to this route

    def add_vehicle_to_route(self, vehicle):
        self.vehicles[vehicle.vehicle_id] = vehicle


# ==========================================
# 2. SYSTEM MANAGER (Functional Requirements)
# ==========================================

class SchoolTransportSystem:
    def __init__(self):
        self.learners = {}  # Store learners by ID
        self.vehicles = {}  # Store all vehicles by ID
        self.routes = {}    # Store routes by ID

    # Req 1: Register learners
    def register_learner(self, learner_id, name):
        if learner_id not in self.learners:
            self.learners[learner_id] = Learner(learner_id, name)
            print(f"Registered Learner: {name}")
        else:
            print("Learner ID already exists.")

    # Req 2: Add transport vehicles and their capacities
    def add_vehicle(self, vehicle_type, vehicle_id, capacity):
        if vehicle_type.lower() == 'bus':
            vehicle = Bus(vehicle_id, capacity)
        elif vehicle_type.lower() == 'minibus':
            vehicle = Minibus(vehicle_id, capacity)
        elif vehicle_type.lower() == 'van':
            vehicle = Van(vehicle_id, capacity)
        else:
            print("Invalid vehicle type.")
            return

        self.vehicles[vehicle_id] = vehicle
        print(f"Added {vehicle_type.capitalize()} (ID: {vehicle_id}, Capacity: {capacity})")

    # Req 3: Create and manage transport routes
    def create_route(self, route_id, name, distance):
        self.routes[route_id] = Route(route_id, name, distance)
        print(f"Created Route: {name} ({distance} km)")

    def assign_vehicle_to_route(self, vehicle_id, route_id):
        if vehicle_id in self.vehicles and route_id in self.routes:
            self.routes[route_id].add_vehicle_to_route(self.vehicles[vehicle_id])
            print(f"Assigned Vehicle {vehicle_id} to Route {route_id}")

    # Req 4 & 5: Assign learners (and Prevent assignment if full)
    def assign_learner(self, learner_id, route_id, vehicle_id):
        learner = self.learners.get(learner_id)
        route = self.routes.get(route_id)
        
        if not learner or not route:
            print("Learner or Route not found.")
            return

        vehicle = route.vehicles.get(vehicle_id)
        if not vehicle:
            print("Vehicle not assigned to this route.")
            return

        # Req 5: Prevent assignment when vehicle capacity is reached
        if vehicle.add_passenger(learner):
            print(f"Success: {learner.name} assigned to Vehicle {vehicle_id} on Route '{route.name}'.")
        else:
            print(f"Failed: Vehicle {vehicle_id} is FULL! Cannot assign {learner.name}.")

    # Req 6: Remove a learner from a transport assignment
    def remove_learner(self, learner_id, route_id, vehicle_id):
        try:
            vehicle = self.routes[route_id].vehicles[vehicle_id]
            if vehicle.remove_passenger(learner_id):
                print(f"Removed Learner {learner_id} from Vehicle {vehicle_id}.")
            else:
                print("Learner not found in this vehicle.")
        except KeyError:
            print("Route or Vehicle not found.")

    # Req 7: Display passengers assigned to each vehicle or route
    def display_passengers(self, route_id):
        route = self.routes.get(route_id)
        if route:
            print(f"\n--- Passengers for Route: {route.name} ---")
            for v_id, vehicle in route.vehicles.items():
                print(f" Vehicle {v_id} ({type(vehicle).__name__}):")
                if not vehicle.passengers:
                    print("   [Empty]")
                for p in vehicle.passengers:
                    print(f"   - {p}")
            print("---------------------------------------")

    # Req 8: Calculate operating costs according to vehicle type
    def display_route_costs(self, route_id):
        route = self.routes.get(route_id)
        if route:
            print(f"\n--- Operating Costs for Route: {route.name} ({route.distance} km) ---")
            total_cost = 0
            for v_id, vehicle in route.vehicles.items():
                # Polymorphism in action here!
                cost = vehicle.calculate_operating_cost(route.distance)
                total_cost += cost
                print(f" Vehicle {v_id} ({type(vehicle).__name__}): ${cost:.2f}")
            print(f" Total Route Cost: ${total_cost:.2f}")
            print("-------------------------------------------------------")

    # Req 9: Display route and vehicle occupancy summaries
    def display_summary(self):
        print("\n========== SYSTEM OCCUPANCY SUMMARY ==========")
        for r_id, route in self.routes.items():
            print(f"Route: {route.name} (ID: {r_id})")
            for v_id, vehicle in route.vehicles.items():
                occ_percentage = (len(vehicle.passengers) / vehicle.capacity) * 100
                print(f"  -> Vehicle {v_id} | Type: {type(vehicle).__name__} | "
                      f"Occupancy: {len(vehicle.passengers)}/{vehicle.capacity} ({occ_percentage:.1f}%)")
        print("==============================================")


# ==========================================
# 3. DRIVER CODE (Testing the requirements)
# ==========================================
if __name__ == "__main__":
    # Initialize the system
    sys = SchoolTransportSystem()

    print("\n--- Req 1 & 2 & 3: Setup System ---")
    sys.register_learner("L01", "Alice Data")
    sys.register_learner("L02", "Bob Analytics")
    sys.register_learner("L03", "Charlie Python")
    
    # Adding vehicles with different capacities
    sys.add_vehicle("van", "V-01", capacity=2)
    sys.add_vehicle("bus", "B-01", capacity=50)

    # Creating routes
    sys.create_route("R1", "North City Loop", distance=20.5)
    
    # Assign vehicles to routes
    sys.assign_vehicle_to_route("V-01", "R1")
    sys.assign_vehicle_to_route("B-01", "R1")

    print("\n--- Req 4 & 5: Assignments (Testing Capacity) ---")
    sys.assign_learner("L01", "R1", "V-01") # Alice into Van
    sys.assign_learner("L02", "R1", "V-01") # Bob into Van (Van is now full - cap 2)
    sys.assign_learner("L03", "R1", "V-01") # Charlie into Van (Should fail - Req 5)
    sys.assign_learner("L03", "R1", "B-01") # Charlie into Bus (Should succeed)

    print("\n--- Req 7: Display Passengers ---")
    sys.display_passengers("R1")

    print("\n--- Req 6: Remove Learner ---")
    sys.remove_learner("L01", "R1", "V-01") # Remove Alice
    sys.display_passengers("R1")            # Show updated passengers

    print("\n--- Req 8: Calculate Operating Costs ---")
    # Shows polymorphism: Bus and Van calculate costs differently based on their classes
    sys.display_route_costs("R1")

    print("\n--- Req 9: Occupancy Summary ---")
    sys.display_summary()