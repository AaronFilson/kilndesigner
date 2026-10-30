#!/usr/bin/env bash
# Docker on a small Mac: run Colima's VM at a size the Mac can spare and at a low priority, and
# stop it when it isn't needed, since it holds on to the memory it has used until it stops.
#
#   scripts/colima.sh start   start the VM at the size set in .env, then lower its priority
#   scripts/colima.sh nice    lower the priority of a VM started some other way
#   scripts/colima.sh stop    stop this app, then the VM and anything else running in it
#
# Each setting comes from the environment, then .env (see small-machine.env), then the default
# here. Only a VM run by QEMU has its priority lowered: Colima uses QEMU on macOS 12, and on
# later versions when started with --vm-type qemu.

set -euo pipefail
cd "$(dirname "$0")/.."

# .env is read, not run: it's a Compose file, and the environment wins over it, as in Compose
setting() {
  local value=${!1:-}
  if [[ -z $value && -f .env ]]; then
    value=$(sed -n "s/^$1=//p" .env | tail -n 1 | tr -d "\"'\r")
  fi
  echo "${value:-$2}"
}
cpus=$(setting KILNDESIGNER_VM_CPUS 2)
memory=$(setting KILNDESIGNER_VM_MEMORY 4)
priority=$(setting KILNDESIGNER_VM_NICE 10)

lower_priority() {
  local pids
  pids=$(pgrep -f 'qemu-system.* -name lima-colima ' || true)
  if [[ -z $pids ]]; then
    echo "Colima's VM isn't running under QEMU, so its priority is left as it is." >&2
    return 1
  fi
  # shellcheck disable=SC2086  # one argument per process
  if ! renice "$priority" -p $pids >/dev/null 2>&1; then
    echo "Couldn't set the VM's priority to $priority (0 to 20). Only root can raise a" \
      "priority, so to raise it, stop and start the VM." >&2
    return 1
  fi
  echo "Colima's VM runs at priority $priority, so the Mac comes first."
}

case ${1:-} in
  start)
    if colima status >/dev/null 2>&1; then
      echo "Colima is already running at the size it was started with; to resize it, stop it first."
    else
      colima start --cpu "$cpus" --memory "$memory"
    fi
    lower_priority || true # the VM is up either way
    ;;
  nice)
    lower_priority
    ;;
  stop)
    # Stopped by hand, the app's containers stay stopped the next time the VM starts
    docker compose stop || true
    colima stop
    ;;
  *)
    echo "usage: $0 start|nice|stop" >&2
    exit 2
    ;;
esac
