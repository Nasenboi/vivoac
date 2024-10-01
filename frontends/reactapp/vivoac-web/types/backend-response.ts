import {z} from 'zod';

export const Backend_Response = z.object({
    api_version: z.string(),
    data: z.any().optional(),
});