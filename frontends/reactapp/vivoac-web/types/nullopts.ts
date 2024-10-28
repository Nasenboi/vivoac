import {z} from 'zod';

export const nullOptString = z.string().nullable().optional().default(undefined);

export const nullEmail = z.union([
    z.string().email(),
    z.string().nullable().optional().default(undefined)
]).default(undefined);