import queue
import threading

from builder import Builder
from cd.update import Update


class CD:
    def __init__(self, system, continuous_deployment=False):
        if not system:
            raise Exception(f"The system {system} cannot be empty!")
        self.system = system

        if type(continuous_deployment) != bool:
            raise Exception(
                f"The continuous_deployment {continuous_deployment} is not bool!"
            )
        self.continuous_deployment = continuous_deployment

        self.is_start_flag = False
        self.updating_map = dict()
        self.prioritize_updating_queue = queue.PriorityQueue()

        modules_path = self.system.get_modules_path()
        response = Builder.get_git_head_hash(path=modules_path)
        is_git_head_hash_invalid = response.get("process").get("returncode")
        if is_git_head_hash_invalid:
            raise Exception(
                f"The is_git_head_hash {is_git_head_hash_invalid} is not valid!"
            )
        self.git_head_hash = response.get("result").strip()
        self.lock = threading.Lock()

    def get_system(self):
        return self.system

    def is_continuous_deployment_active(self):
        return self.continuous_deployment

    def is_start(self):
        return self.is_start_flag

    def get_git_head_hash(self):
        return self.git_head_hash

    def get_lock(self):
        return self.lock

    def start(self):
        threading.Thread(target=self.build).start()

        self.is_start_flag = True

    def create_updates(self, changed_files):
        if changed_files == None:
            raise Exception(f"The changed_files {changed_files} cannot be empty!")

        if type(changed_files) != list:
            raise Exception(f"The changed_files {changed_files} is not list!")

        updates = []
        for changed_file in changed_files:
            if "modules" not in changed_file:
                continue

            modules_path = self.system.get_modules_path()
            modules_index = changed_file.index("modules") + len("modules")
            if not modules_path.endswith(changed_file[:modules_index]):
                continue

            parts = changed_file[modules_index + 1 :].split("/")
            module_name = parts[0]
            version_name = parts[1]

            module = self.system.get_module(module_name)
            if not module:
                continue

            version = module.get_version(version_name)
            if not version:
                continue

            update = Update(version)
            updates.append(update)

        return updates

    def put_update(self, update):
        if not update:
            raise Exception(f"The update {update} cannot be empty!")

        update_id = update.get_id()
        if self.updating_map.get(update_id):
            return

        self.prioritize_updating_queue.put(update)
        self.updating_map[update_id] = True

    def put_updates(self, updates):
        if updates == None:
            raise Exception(f"The updates {updates} cannot be empty!")

        if type(updates) != list:
            raise Exception(f"The updates {updates} is not list!")

        for update in updates:
            self.put_update(update)
            self.system.logger.info(f"{update} was added to priority queue.")

    def update(self):
        self.lock.acquire()
        modules_path = self.system.get_modules_path()
        response = Builder.git_pull(path=modules_path)
        is_git_pull_invalid = response.get("process").get("returncode")
        if is_git_pull_invalid:
            raise Exception(f"The is_git_pull {is_git_pull_invalid} is not valid!")

        response = Builder.get_git_files_changes(
            self.git_head_hash,
            path=modules_path,
        )
        is_git_files_changes_invalid = response.get("process").get("returncode")
        if is_git_files_changes_invalid:
            raise Exception(
                f"The is_git_files_changes {is_git_files_changes_invalid} is not valid!"
            )
        changed_files = response.get("result").split()

        updates = self.create_updates(changed_files)
        self.put_updates(updates)

        response = Builder.get_git_head_hash(path=modules_path)
        is_git_head_hash_invalid = response.get("process").get("returncode")
        if is_git_head_hash_invalid:
            raise Exception(
                f"The is_git_head_hash {is_git_head_hash_invalid} is not valid!"
            )
        self.git_head_hash = response.get("result").strip()
        self.lock.release()

    def build(self):
        while True:
            try:
                if not self.prioritize_updating_queue.empty():
                    update = self.prioritize_updating_queue.get()
                    update.build()

                    self.system.logger.info(f"{update} was built.")

            except Exception as e:
                self.put_update(update)

    def __str__(self):
        cd_status = "start" if self.is_start_flag else "not start"
        return f"<CD ({cd_status}) in the last git head hash {self.git_head_hash}>"
