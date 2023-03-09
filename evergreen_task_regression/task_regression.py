"""see details of an evergreen task, variants with their

Usage:
    task_regression.py (--project PROJECT) (--tasks TASKS) [--variants VARIANTS] [--period PERIOD] [--monthly | --weekly | --biweekly] [--verbose]

Options:
    --project PROJECT       evergreen project id
    --tasks TASKS           comma separated evergreen task list
    --variants VARIANTS     comma separated evergreen variant list
    --period PERIOD         the period of time the task performance will be calculated (default: 30)
    --monthly               group task performance by month
    --weekly                group task performance by week
    --biweekly              group task performance by 14 days
    --verbose               debug level for the logger
"""

import os
import logging
from logging import StreamHandler
from datetime import date, timedelta, datetime
from typing import List, Dict, Any, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined

from docopt import docopt

from evergreen.api import EvergreenApi, EvgAuth
from evergreen.stats import TaskStats


logger = logging.getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(logging.INFO)


def _get_task_stats(
        evergreen_api: EvergreenApi,
        after_date: datetime,
        before_date: datetime,
        project: str,
        tasks: List[str],
        variants: Optional[List[str]],
        group_num_days: int
):
    if variants:
        task_status: List[TaskStats] = evergreen_api.task_stats_by_project(
            after_date=datetime(after_date.year, after_date.month, after_date.day),
            before_date=datetime(before_date.year, before_date.month, before_date.day),
            project_id=project,
            tasks=tasks,
            variants=variants,
            group_num_days=group_num_days,
            group_by="task_variant",
        )
    else:
        task_status: List[TaskStats] = evergreen_api.task_stats_by_project(
            after_date=datetime(after_date.year, after_date.month, after_date.day),
            before_date=datetime(before_date.year, before_date.month, before_date.day),
            project_id=project,
            tasks=tasks,
            group_num_days=group_num_days,
            group_by="task_variant"
        )

    return task_status


def _organize_stats_by_task_variant(
        stats_by_task_variant: Dict[str, List[TaskStats]],
        task_status: List[TaskStats]
):
    for stat in task_status:
        key = f"{stat.task_name}-{stat.variant}"
        if key not in stats_by_task_variant:
            stats_by_task_variant[key] = []
        stats_by_task_variant[key].append(stat)


def _compute_time_regression(stats_by_task_variant: Dict[str, List[TaskStats]]):
    for task_variant in stats_by_task_variant:
        task_stats: List[TaskStats] = stats_by_task_variant[task_variant]
        avg_duration_passes = list(map(lambda stat: stat.avg_duration_pass, task_stats))
        min_duration = min(avg_duration_passes)
        max_duration = max(avg_duration_passes)
        percentage_min_max = float((max_duration - min_duration) / min_duration) * 100
        if percentage_min_max >= 10:
            logger.warning({
                "message": "Max time for task regressed by more than 10%",
                "task_variant": task_variant,
                "min_duration": f"{round(min_duration, 2)}secs",
                "max_duration": f"{round(max_duration, 2)}secs",
                "regression": round(percentage_min_max, 2)
            })

        regression_from_min = map(
            lambda stat: float((stat.avg_duration_pass - min_duration) / min_duration) * 100,
            task_stats
        )
        for idx, reg in enumerate(regression_from_min):
            if reg >= 10:
                logger.warning({
                    "message": "Task duration regressed by more than 10% from min duration",
                    "task_date": task_stats[idx].date,
                    "min_duration": f"{round(min_duration, 2)}secs",
                    "task_duration": f"{round(task_stats[idx].avg_duration_pass, 2)}secs",
                    "regression": round(reg, 2)
                })


def _task_regression(arguments: Dict[str, Any]):
    project: str = arguments["--project"]
    tasks = arguments["--tasks"]
    task_list = tasks.split(",")
    variants: Optional[str] = arguments.get("--variants", None)
    variant_list = variants.split(",") if variants else None
    cadence: int = 7
    if arguments.get("--monthly", False):
        cadence = 30
    elif arguments.get("--biweekly", False):
        cadence = 14
    else:
        cadence = 7

    period = int(arguments.get("--period", 30))
    after_date = (date.today() - timedelta(days=period))
    before_date = (after_date + timedelta(days=cadence))

    evergreen_user = os.getenv("EVERGREEN_USER")
    evergreen_password = os.getenv("EVERGREEN_PASSWORD")

    evergreen_api = EvergreenApi.get_api(EvgAuth(evergreen_user, evergreen_password))
    logger.debug({
        "message": "Created Evergreen client",
        "evergreen_api": evergreen_api,
    })

    stats_by_task_variant: Dict[str, List[TaskStats]] = {}

    while True:
        _organize_stats_by_task_variant(
            stats_by_task_variant,
            _get_task_stats(
                evergreen_api=evergreen_api,
                after_date=datetime(after_date.year, after_date.month, after_date.day),
                before_date=datetime(before_date.year, before_date.month, before_date.day),
                project=project,
                tasks=task_list,
                variants=variant_list,
                group_num_days=cadence
            ))
        period = period - cadence
        if period <= 0:
            break
        after_date = before_date
        before_date = (after_date + timedelta(days=cadence))

    _compute_time_regression(stats_by_task_variant)


if __name__ == "__main__":
    logger.info({
        "message": "Attempting to find task regression"
    })

    args: Dict[str, Any] = docopt(__doc__)
    if args["--verbose"]:
        logger.setLevel(logging.DEBUG)

    logger.debug({
        "message": "task regression arguments",
        "arguments": args
    })

    _task_regression(args)
