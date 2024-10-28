import {z} from 'zod';

export const nullOptString = z.string().nullable().optional().default(undefined);

export const nullEmail = z.union([
    z.literal(''),
    z.string().email(),
]).default(undefined);