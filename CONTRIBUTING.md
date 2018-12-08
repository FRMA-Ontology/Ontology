#### Contributing to the FRMA Ontology

This document will walk you through the steps of setting up your computer for contributing to the FRMA Ontology.



#### First Steps

1. Make sure [Git](https://git-scm.com/) is installed on your local system

2. Download and install [Protege](https://protege.stanford.edu/).



#### Development Environment Setup

1. Fork the [FRMA-Ontology/Ontology](https://github.com/FRMA-Ontology/Ontology) repository on GitHub.

2. Rename your fork of the repository on GitHub to `FRMA-Ontology` (otherwise it will just be called `yourusername/Ontology`, which doesn't adequately describe the repository.)

3. Clone your fork of the repository, (i.e. 'yourusername/FRMA-Ontology`). Use `Clone with SSH` from the `Clone or download` dropdown on GitHub with the following terminal command:

`git clone git@github.com:yourusername/FRMA-Ontology.git`

4. Navigate into the `FRMA-Ontology` directory (i.e. `cd FRMA-Ontology`) and add the `upstream` remote to the repository:

`git remote add upstream git@github.com:FRMA-Ontology/Ontology.git`

This enables you to pull the latest upstream changes. You can ensure this worked correclty by running `git remote show`. You should see entries for both `origin` and `upstream`.

5. Create and checkout a `dev` branch:

- `git branch dev`
- `git checkout dev`

**Now you can start developing features!**



#### Developing

TODO - flesh out this section a bit.
- Opening the file in Protege
- Check our [open issues](https://github.com/FRMA-Ontology/Ontology/issues)
- [Open a new issue](https://github.com/FRMA-Ontology/Ontology/issues/new)



#### Commiting Changes

To commit your changes, do the following steps:

1. Check the status of your changes

You can view the status of your latest changes using the following command:
`git status`

2. Stage your changes for the next commit

You can stage all your changes for the next commit with the following command:
`git add .`

3. Commit your changes

Commit your changes with an inline message with the following command:
`git commit -m "Fixed type in ImageOntology.rdf"`

4. Push your changes

You can push your commited changes to your `dev` branch with the following command:
`git push origin dev`



#### Merging Changes

1. Navigate [here](https://github.com/FRMA-Ontology/Ontology/compare) to open a new pull request into the [FRMA-Ontology/Ontology](https://github.com/FRMA-Ontology/Ontology) GitHub repository

2. Click `Compare across forks` and select you fork (i.e. `yourusername/FRMA-Ontology`) from the dropdown

3. Make sure that you're opening your PR from your `dev` branch into the `rcos/observatory` `dev` branch

4. Reference the GitHub issue inside the pull request comment with `#787`, with `787` being the GitHub issue number

5. Click `Create Pull Request` and your code will be reviewed by an administrator.
