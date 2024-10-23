# SPDX-License-Identifier: Apache-2.0
#
# http://nexb.com and https://github.com/aboutcode-org/scancode.io
# The ScanCode.io software is licensed under the Apache License version 2.0.
# Data generated with ScanCode.io is provided as-is without warranties.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# Data Generated with ScanCode.io is provided on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. No content created from
# ScanCode.io should be considered or used as legal advice. Consult an Attorney
# for any legal advice.
#
# ScanCode.io is a free software code scanning tool from nexB Inc. and others.
# Visit https://github.com/aboutcode-org/scancode.io for support and download.


from packageurl import PackageURL

from scanpipe.pipelines import Pipeline
from scanpipe.pipes import federatedcode


class PublishToFederatedCode(Pipeline):
    """Publish package scan to FederatedCode."""

    download_inputs = False
    is_addon = True

    @classmethod
    def steps(cls):
        return (
            cls.get_project_purl,
            cls.get_package_repository,
            cls.clone_repository,
            cls.add_scan_result,
            cls.commit_and_push_changes,
            cls.delete_local_clone,
        )

    def get_project_purl(self):
        """Get the PURL for the project."""
        all_executed_pipeline_successful = all(
            run.task_succeeded for run in self.project.runs.executed()
        )

        source_is_download_url = any(
            source.download_url for source in self.project.inputsources.all()
        )

        if not all_executed_pipeline_successful:
            raise Exception("Make sure all the pipelines has completed successfully.")

        if not source_is_download_url:
            raise Exception("Project input should be download_url.")

        if not self.project.project_purl:
            raise Exception("Missing Project PURL.")

        project_package_url = PackageURL.from_string(self.project.project_purl)

        if not project_package_url.version:
            raise Exception("Missing version in Project PURL.")

        configured, error = federatedcode.is_configured()
        if not configured:
            raise Exception(error)

        self.project_package_url = project_package_url

    def get_package_repository(self):
        """Get the Git repository URL and scan path for a given package."""
        self.package_git_repo, self.package_scan_file = (
            federatedcode.get_package_repository(
                project_purl=self.project_package_url, logger=self.log
            )
        )

    def clone_repository(self):
        """Clone repository to local_path."""
        self.repo = federatedcode.clone_repository(
            repo_url=self.package_git_repo,
            logger=self.log,
        )

    def add_scan_result(self):
        """Add package scan result to the local Git repository."""
        self.relative_file_path = federatedcode.add_scan_result(
            project=self.project,
            repo=self.repo,
            package_scan_file=self.package_scan_file,
            logger=self.log,
        )

    def commit_and_push_changes(self):
        """Commit and push changes to remote repository."""
        federatedcode.commit_and_push_changes(
            repo=self.repo,
            file_to_commit=str(self.relative_file_path),
            purl=str(self.project_package_url),
            logger=self.log,
        )
        self.log(
            f"Scan result for '{str(self.project_package_url)}' "
            f"pushed to '{self.package_git_repo}'"
        )

    def delete_local_clone(self):
        """Remove local clone."""
        federatedcode.delete_local_clone(repo=self.repo)
