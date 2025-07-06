# ℹ️ Reminder

- **Workspace ID**: Enter the **numeric Workspace ID**, and only one workspace can be entered at a time. This ID is the unique identifier for your workspace within the system. Please ensure that you enter the correct Workspace ID for the data you wish to access.

- **Storefront EID**: Enter one or more **Storefront IDs** (unique identifiers for storefronts), separated by commas. You can input multiple storefront IDs at once, but **all storefronts must belong to the same workspace** (the workspace ID entered above).  
  - **Important Note**: When entering multiple Storefront IDs, ensure that all storefronts are within the same **workspace** to avoid errors in the data query.  
  - If you enter **one Storefront ID**, the system will only export data for that specific storefront.

- **Start Date** and **End Date**: Select the date range from **yesterday** to **30 days ago**.  
  - **Start Date**: The beginning date of the period for which you wish to export data.  
  - **End Date**: The end date of the period for which you wish to export data.  
  - **Note**: Ensure that the **End Date** is not earlier than the **Start Date**, and the selected dates must fall within the range from yesterday to 30 days ago.

- **Large Datasets**: If you are exporting a large dataset (e.g., more than 20,000 rows), the export process may take some time. In this case, the system will prompt you to confirm before proceeding, so you are aware that it might take longer to load and export the data.  
  - **Important**: If the number of rows exceeds **50,000**, consider reducing the number of storefronts selected to ensure the database remains stable during the export process. **Don't be lazy!**

- **Search Volume**: By default, the data will include only records where the search volume is **greater than 0**. This ensures that the export will not overload the database and will maintain data integrity.
- **Downloading Data**: When you click the "Download" button, please **wait a moment** for the data to be downloaded. The file will automaticaly place in your folder and initially be in a **CRSWAP format**, and once the download is complete, it will automatically be converted into a **CSV format**.
