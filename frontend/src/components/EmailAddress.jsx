import {TextField} from "@mui/material";
import {useState} from "react";

const errorText = 'Email addresses should be longer than 10 characters, contain an @ symbol and should contain a domain.'
const defaultText = 'You can enter numbers, letters and periods'

// https://stackoverflow.com/questions/52188192/what-is-the-simplest-and-shortest-way-for-validating-an-email-in-react
const validateEmail = (email) => {
    const regexp = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return regexp.test(email);
}


const EmailAddress = ({placeholder, email, setValue, errorInInputs, setErrorInInputs, errorKey}) => {

    const [helperText, setHelperText] = useState(defaultText);

    const checkEmailAddress = (event) => {
        const emailAddress = event.target.value;
        if (!validateEmail(emailAddress)) {
            setErrorInInputs({...errorInInputs, [errorKey]: false})
            setHelperText(errorText)
        } else {
            setErrorInInputs({...errorInInputs, [errorKey]: true})
            setHelperText(defaultText)
        }
    }

    return (
        <>
            <TextField
                variant={"outlined"}
                placeholder={placeholder}
                fullWidth={true}
                sx={{width: "350px"}}
                value={email}
                onChange={setValue}
                error={!errorInInputs[errorKey]}
                onBlur={checkEmailAddress}
                helperText={helperText}
            />
        </>
    )
}

export default EmailAddress;