import { z } from 'zod';
import { nullOptString, nullEmail } from './nullopts';
import { Address } from './address';

export const ViVoAc_Voice_Talent = z.object({
    created_at: nullOptString,
    updated_at: nullOptString,
    _id: nullOptString,
    first_name: nullOptString,
    last_name: nullOptString,
    email: nullEmail,
    voices: z.array(z.string()).nullable().optional(),
    birth_date: nullOptString,
    gender: nullOptString,
    address: Address.nullable().optional(),
    phone_number_home: nullOptString,
    phone_number_mobile: nullOptString,
});

export const ViVoAc_Voice_Talent_Gender_Options = [
    {
        value: "male",
        label: "Male",
    },
    {
        value: "female",
        label: "Female",
    },
    {
        value: "transgender",
        label: "Transgender",
    },
    {
        value: "non-binary",
        label: "non-binary",
    },
];