USE parkingDB;

CREATE TABLE parking_lot_info (
    parking_code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(200),
    type_name VARCHAR(50),
    operation_type_name VARCHAR(50),
    phone VARCHAR(20),
    info_provide_name VARCHAR(255),
    total_spots INT,
    fee_type_name VARCHAR(20),
    night_free_name VARCHAR(10)
);

ALTER TABLE parking_lot_info ADD COLUMN latitude DOUBLE;
ALTER TABLE parking_lot_info ADD COLUMN longitude DOUBLE;

CREATE TABLE parking_lot_operation (
    parking_code VARCHAR(20) PRIMARY KEY,
    weekday_start VARCHAR(4),
    weekday_end VARCHAR(4),
    weekend_start VARCHAR(4),
    weekend_end VARCHAR(4),
    holiday_start VARCHAR(4),
    holiday_end VARCHAR(4),
    sat_fee_type_name VARCHAR(20),
    holiday_fee_type_name VARCHAR(20),
    FOREIGN KEY (parking_code) REFERENCES parking_lot_info(parking_code)
);

CREATE TABLE parking_lot_fee (
    parking_code VARCHAR(20) PRIMARY KEY,
    basic_fee INT,
    basic_time INT,
    extra_fee INT,
    extra_time INT,
    daily_max_fee INT,
    FOREIGN KEY (parking_code) REFERENCES parking_lot_info(parking_code)
);

CREATE TABLE parking_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parking_code VARCHAR(20),
    current_cars INT,
    update_time DATETIME NOT NULL
);
