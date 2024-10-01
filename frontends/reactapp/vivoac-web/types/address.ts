import { z } from 'zod';
import { nullOptString } from './nullopts';

export const Address = z.object({
    street: nullOptString,
    city: nullOptString,
    state: nullOptString,
    country: nullOptString,
    postal_code: nullOptString,
});