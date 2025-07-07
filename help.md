# ℹ️ **Some Important Notes**

- **Workspace ID**: Enter the **numeric Workspace ID**, which is the unique identifier for your workspace in the system. You can only enter **one workspace** at a time.  
  - **Tip**: Ensure you input the correct Workspace ID to avoid data discrepancies. Double-check it!

- **Storefront EID**: Enter one or more **Storefront IDs** (unique identifiers for storefronts) separated by commas. Multiple storefronts are allowed, but **all storefronts must belong to the same workspace**.  
  - **Important**: If you enter **multiple Storefront IDs**, make sure they belong to the **same workspace**. Mismatched storefronts across different workspaces will cause missing data.
  - If you enter **one Storefront ID**, the system will only export data for that specific storefront.

- **Start Date** and **End Date**: Select the date range between **yesterday** and **30 days ago**.  
  - **Start Date**: The starting date for the data export.  
  - **End Date**: The ending date for the data export.  
  - **Note**: The **End Date** should not be earlier than the **Start Date**, and the selected dates should fall within the last **30 days**.

- **Large Datasets**: If you're exporting a large dataset (e.g., more than **20,000 rows**), the process might take some time. The system will prompt you to confirm before proceeding.  
  - **Important**: If the dataset exceeds **50,000 rows**, it is recommended to **reduce the number of storefronts** selected, as large datasets can impact the system’s stability.  
  - **Reminder**: Large datasets can cause delays in exporting or slow database performance. Be patient!

- **Search Volume**: By default, the data export will include only records where the search volume is **greater than 0**. This ensures optimal system performance and prevents overwhelming the database.  

- **Downloading Data**: When you click the "Download" button, please **wait a moment** for the data to process. Once completed:
  - The data will **automatically** download and place directly in your folder with a **CRSWAP format**.
  - The file will **then** convert into a **CSV format** after download completion.

---

## Additional Information

- **Data Integrity**: To maintain data integrity, avoid making changes to the exported file after download, especially when dealing with large or complex datasets.
- **Performance Tip**: If you consistently export large datasets, consider splitting your exports into smaller time intervals or storefront groups to maintain smoother performance.
- **Technical Support**: If you encounter issues during the export or with the data file or you want to request a new type of export, please speak directly to **[IrvineCao](https://epsilo.slack.com/archives/D075WP12FJ5)** for assistance.

---
