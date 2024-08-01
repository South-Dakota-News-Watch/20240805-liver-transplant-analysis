# 20240805-liver-transplant-analysis
This repository includes a [code notebook](liver-transplant-findings.ipynb) and supporting documentation to reproduce the findings in ["TK,"](TK) an article by Megan Luther published Aug. 5, 2024, for South Dakota News Watch. Cody Winchester analyzed the data.

- [Data overview](#Data-overview)
- [Running the notebook](#Running-the-notebook)

## Data overview
The United Network for Organ Sharing (UNOS) provided us with a copy of its [STAR file](https://optn.transplant.hrsa.gov/data/view-data-reports/request-data/) (tab-delimited version) on July 31, 2024. Access to the data and documentation requires a signed data use agreement with UNOS, so we're not including those files here. [The public data dictionary is here](https://optn.transplant.hrsa.gov/media/1swp2gge/optn-star-files-data-dictionary.xlsx) (XLSX).

Data coverage is October 1987 through June 2024, though our analysis looks only at data beginning in listing year 1988, the first full year of data.

The main files for data on transplants for each organ system are tab-delimited `.DAT` files without headers. The [`get_df() function in utils.py`](utils.py) reads in column names from the `.htm` files that accompany each `.DAT` file and uses these to build a pandas dataframe.

Our analysis focused on the `LIVER_DATA.DAT` file, which

>Includes one record per liver waiting list registration and/or transplant. Includes livers used in multivisceral transplants. If the patient received a living donor transplant without being placed on the waiting list, there will be transplant information but no waiting list information. If the patient was listed for transplant but not transplanted as a result of that registration, there will be waiting list information but no transplant data.

(Quotes are from the `National STAR file user guide.pdf` documentation.)

In the main data file for each organ, such as `LIVER_DATA.DAT`, each row is an _event_ in the waiting list/transplant process, not a unique organ donation candidate. Each file

>contains information on all waiting list registrations and transplants of that organ type that have been listed or performed in the United States since October 1, 1987. It includes both deceased and living donor transplants. There is one record per waiting list registration/transplant event, and each record includes the most recent follow-up information (including patient and graft survival) reported to the OPTN as of the date the file was created. If a patient was listed for a transplant, but was removed prior to a transplant related to that registration, or is still waiting, all the transplant information for that patient is null (i.e., there are waiting list records in the dataset with no transplant information). Similarly, if a patient received a living donor transplant, and was never on the waiting list, all of the waiting list-specific information for that patient is null (i.e., there are transplant records in the dataset with no waiting list information). Waiting list registrations can be selected by choosing records where WL_ID_CODE is not null, and transplants performed can be selected by choosing records where TRR_ID_CODE is not null. If there was a waiting list registration that resulted in a transplant event, neither WL_ID_CODE nor TRR_ID_CODE will be null. Recently introduced variables VAL_DT_TCR and VAL_DT_TRR provide information about when the Transplant Candidate Registration and Transplant Recipient Registration were validated. These variables might be null for more recent registrations and transplants.

So if a candidate recieved a transplant, the value in the field `TRR_ID_CODE` will be populated. We took the additional precaution of setting a `has_tx` flag on _every_ event record tied to a candidate who ultimately got a transplant, to ensure that deduplicating records by candidate ID didn't inadvertantly lose this information.

Candidates are uniquely identified by the value in the `PT_CODE` field:
>The files in the standard datasets ... [include] an encrypted patient identification number (PT_CODE), unique to each patient that allows you to track the patient through multiple waiting list and transplant events.

Each candidate can be tied to multiple events in the dataset. To count the number of unique candidates for transplant of a given organ, we count the number of unique `PT_CODE` values in the data (or subset of data). Candidates can also be tied to multiple uniquely identified transplants of the same organ (re-transplants).

In cases where we needed to deduplicate the data to examine an individual candidates' record(s), we selected the most recent record based on the `PX_STAT_DATE` value.

The data include both living and dead donors. Donors are uniquly identifed by the value in the `DONOR_ID` column.

### Alcohol use
UNOS doesn't collect data on alcohol use by candidates specifically, although, according to an email from UNOS,
>Especially for liver transplant candidates, I believe many centers have requirements for their candidates that they abstain from alcohol use as a condition of being listed.

To identify donor candidates who were listed with a diagnosis associated with an alcohol-related disease, we filtered based on the diagnostic codes associated with alcohol-related disease (found in fields `DGN_TCR`, `DGN2_TCR`, or `DIAG`). According to UNOS, these are:
- 4215 – Alcoholic Cirrhosis
- 4216 – Alcoholic Cirrhosis with Hepatitis C
- 4217 – Acute Alcoholic Hepatitis
- 4218 – Acute Alcohol-Associated Hepatitis with or without Cirrhosis
- 4219 – Alcohol-Associated Cirrhosis without Acute Alcohol-Associated Hepatitis

The `DIAG` field was collected from 1987 onward, and the `DGN_TCR` and `DGN2_TCR` were collected from 1994 onward, according to the STAR file data dictionary.

## Running the notebook
First, you'll need to [request a copy of the STAR file](https://optn.transplant.hrsa.gov/data/view-data-reports/request-data/) from UNOS. We put the data files in the `data` folder and documentation in the `docs` folder.

- Clone or download this repo and `cd` into the project directory
- Install the dependencies (`jupyterlab`, `pandas` and `bs4`) into a virtual environment: `pip install -r requirements.txt`
- `jupyter lab`
