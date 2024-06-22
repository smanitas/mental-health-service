# Mental Health Service (work edition) 

<img src="https://cdn.revolutionise.com.au/cups/arv/files/jlnephtwte1m2zah.png" alt="Mental Health Illustration" width="350"/>

## Overview

This service sends daily nature images and inspirational quotes to colleagues, boosting their mental well-being.

## How It Works

1. **Fetch Quote**: The service retrieves an inspirational quote from a Quotable API.
2. **Fetch Image**: A random nature image is fetched from Unsplash API.
3. **Overlay Quote**: The quote is overlaid on the image using the Pillow library.
4. **Automated Delivery**: The final image with the overlaid quote is sent to users via MS Teams channel.
5. **Airflow Integration**: Apache Airflow schedules and manages workflow sending pictures every day except some holidays.

## Example

[See Example](https://drive.google.com/file/d/1LeJHCE67z3UcJFw6-eTzwFdEvy6spFkE/view?usp=sharing)
