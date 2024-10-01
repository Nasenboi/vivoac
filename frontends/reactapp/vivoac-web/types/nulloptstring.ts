import {z} from 'zod';

export const nullOptString = z.string().nullable().optional();