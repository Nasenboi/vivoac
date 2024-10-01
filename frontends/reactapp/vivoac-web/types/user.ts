import { z } from 'zod';
import { nullOptString, nullEmail } from './nullopts';
import { Address } from './address';

export const ViVoAc_User = z.object({
    created_at: nullOptString,
    updated_at: nullOptString,
    _id: nullOptString,
    username: nullOptString,
    first_name: nullOptString,
    last_name: nullOptString,
    email: nullEmail,
    role: nullOptString,
    address: Address.nullable().optional(),
    phone_number_home: nullOptString,
    phone_number_mobile: nullOptString,
    disabled: z.boolean().nullable().optional(),
    config: z.any().nullable().optional(),
    password: nullOptString,
});