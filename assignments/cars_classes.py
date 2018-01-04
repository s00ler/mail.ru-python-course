from os import path
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        return path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        size = body_whl.split('x')
        if size == ['']:
            size = [0, 0, 0]
        self.body_width = float(size[0])
        self.body_height = float(size[1])
        self.body_length = float(size[2])

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    try:
        with open(csv_filename) as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)  # пропускаем заголовок
            for row in reader:
                try:
                    car_type = row[0]
                    if car_type == Car.car_type:
                        car_list.append(Car(row[1], row[3],
                                            float(row[5]), int(row[2])))
                    elif car_type == Truck.car_type:
                        car_list.append(Truck(row[1], row[3],
                                              float(row[5]), row[4]))
                    elif car_type == SpecMachine.car_type:
                        car_list.append(SpecMachine(row[1], row[3],
                                                    float(row[5]), row[6]))
                    else:
                        raise Exception('Unknown car type.')
                except Exception:
                    pass
    except Exception:
        return None
    return car_list
