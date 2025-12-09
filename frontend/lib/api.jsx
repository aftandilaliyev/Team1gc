import { ApiSDK } from "../../sdk/sdk";
import { API_BASE_URL } from "./constants.jsx";

const sdk = new ApiSDK(API_BASE_URL);

export const client = sdk.getApi();