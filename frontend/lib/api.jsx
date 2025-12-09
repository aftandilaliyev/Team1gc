import { ApiSDK } from "@rasadov/team-gc-sdk";
import { API_BASE_URL } from "./constants.jsx";

export const sdk = new ApiSDK(API_BASE_URL);
export const client = sdk.getApi();